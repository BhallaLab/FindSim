# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 

'''
*******************************************************************
 * File:            simWrapMoose.py
 * Description:     MOOSE interface for findSim
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/
 '''


from __future__ import print_function
import re
import os
import ntpath
import numpy as np
import moose
import sys
from importlib import util

# import imp  ## May be deprecated from Python 3.4
# from simWrap import SimWrap 
# from simError import SimError


if sys.version_info < (3, 4):
    import imp      # This is apparently deprecated in Python 3.4 and up
else:
    import importlib   

foundLib_HillTau_ = False

try:
    import hilltau
    foundLib_HillTau_ = True
except Exception as e:
    pass

if __package__ is None or __package__ == '':
    from simError import SimError
    from simWrap import SimWrap

else:
    from FindSim.simError import SimError
    from FindSim.simWrap import SimWrap

MINIMUM_TAU = 1e-3     # Do not permit excessively fast chem time consts.
MINIMUM_TAU_RATIO = 1e-2  # Do not permit excessively large change in tau.
elecDt = 50e-6
elecPlotDt = 100e-6
fepspScale = 1.0e7 # Arb scaling. Need to figure out how to set,
    # Obviously a function of stimulus strength but the experimentalist
    # also typically adjusts stim to get response into a 'useful' range.
    # Should redo in terms of resistivity, but that too is a function of
    # slice geometry.

def isContainer( elm ):
    return elm.className == 'Neutral' or elm.isA[ 'ChemCompt']

def getContainerTree( elm, kinpath ):
    tree = []
    pa = elm.parent
    while (pa.path != kinpath and pa.path != '/'):
        tree.append( pa )
        pa = pa.parent
    return tree

def isNotDescendant( elm, ancestorSet ):
    # Start by getting rid of cases where elm itself is in ancestor set.
    pa = elm
    while (pa.path != '/'):
        if pa.path in ancestorSet:
            return False
        pa = pa.parent
    return True

def findParentGroupPath( elm ):
    if isContainer( elm ):
        return elm.path
    else:
        return findParentGroupPath( elm.parent )

def findLinkSet( parent, allIn ):
    linkSet = set()
    dropSet = set()
    
    #print( " findingLink", parent)
    for ee in moose.wildcardFind( "{0}/##[ISA=EnzBase],{0}/##[ISA=Reac]".format( parent ) ):
        for nn in (ee.neighbors['sub'] + ee.neighbors['prd']):
            pa = findParentGroupPath( nn )
            if pa == "/":
                continue
            elif pa not in allIn:
                #print( " appending", pa, nn.path )
                linkSet.add( pa )
                linkSet.add( nn.path )
                for ff in moose.wildcardFind( "{0}/##[ISA=PoolBase],{0}/##[ISA=EnzBase],{0}/##[ISA=Reac],{0}/##[ISA=Function]".format( pa ) ):
                    dropSet.add( ff.path )

    return linkSet, dropSet


#######################################################################
## Four utility functions to set/get Kd and tau. All assignments should use
## these funcs to retain consistency.
#######################################################################

def getReacKd( elm ):
    if not elm.isA['Reac']:
            raise SimError( "getReacKd: can only get Kd on a Reac, was: '{}' on '{}'".format( elm.className, elm.path ) )
    #print( "getReacKd for {} = {}, concKb/Kf = {}/{} ".format( elm.name, elm.Kb/elm.Kf, elm.Kb, elm.Kf ) )
    return elm.Kb/elm.Kf

def setReacKd( elm, Kd ):
    # Here we want to change the ratio of Kf and Kb while keeping 
    # tau the same.
    if not elm.isA['Reac']:
            raise SimError( "getReacKd: can only set Kd on a Reac, was: '{}' on '{}'".format( elm.className, elm.path ) )
    tau = getReacTau( elm ) # Note func assumption about reac orders 
    #print("PreScaledParam ** KD ** {}.{} Kf={:.4f} Kb={:.4f} tau = {:.4f}  tgtKd = {:.4f}".format( params[0], field, obj.Kf, obj.Kb, tau, Kd) )
    scaleKf = 0.001 ** (elm.numSubstrates-1)
    scaleKb = 0.001 ** (elm.numProducts-1)
    elm.Kf = 1.0 / ( tau * (scaleKb * Kd + scaleKf ) )
    elm.Kb = Kd * elm.Kf
    #print("ScaledParam ** KD ** {}.{} Kf={:.4f} Kb={:.4f} tau = {:.4f}  tgtKd = {:.4f}".format( params[0], field, obj.Kf, obj.Kb, tau, Kd) )

def getReacTau( elm ):
    if not elm.isA['Reac']:
            raise SimError( "getReacTau: can only get tau on a Reac, was: '{}' on '{}'".format( elm.className, elm.path ) )
    # This is a little dubious, because order 1 reac has 1/conc.time
    # units. Suppose Kf = x / mM.sec. Then Kf = 0.001x/uM.sec
    # This latter is the Kf we want to use, assuming typical concs are
    # around 1 uM.
    scaleKf = 0.001 ** (elm.numSubstrates-1)
    scaleKb = 0.001 ** (elm.numProducts-1)
    tau = 1.0 / ( elm.Kb * scaleKb + elm.Kf * scaleKf )
    #print( "TAU = {:.4f}, Kf = {:.4g}, Kb = {:.4g}".format( tau, elm.Kb, elm.Kf, ) )
    #print( "getReacTau for {} = {}, Kb={}, Kf={} ".format( elm.name, tau, elm.Kb, elm.Kf ) )

    return tau

def setReacTau( elm, tau ):
    if not elm.isA['Reac']:
            raise SimError( "setReacTau: can only set tau on a Reac, was: '{}' on '{}'".format( elm.className, elm.path ) )
    # Here we use the form tau = 1/(Kf + Kb) with suitable scaling.
    # If we assume that Kf and Kb contribute equally to tau, we just
    # need to scale them accordingly.
    oldTau = getReacTau( elm )
    if oldTau < MINIMUM_TAU:
        return
    if tau < oldTau * MINIMUM_TAU_RATIO:
        tau = oldTau * MINIMUM_TAU_RATIO
    elm.Kf *= oldTau / tau
    elm.Kb *= oldTau / tau

#######################################################################

class SimWrapMoose( SimWrap ):
    def __init__( self, *args, **kwargs ):
        SimWrap.__init__( self, *args, **kwargs )
        self.plotPath = {}


    def findObj( self, uname, noRaise = False ):
        '''
        Model:: findObj locates objects uniquely specified by a string. 
        The object can be located at any depth in the model tree.
        The identifier string typically consists of the name of an object,
        but it may be necessary to disambiguate it by including its parent
        name as well.
        For example, if there is a foo/bar and a zod/bar, then we will 
        have to pass "zod/bar" to uniquely specify the object.
        '''
        #name = uname.encode( 'ascii' )
        name = uname
        rootpath = self.modelId.path
        try1 = moose.wildcardFind( rootpath+'/' + name )
        try2 = moose.wildcardFind( rootpath+'/##/' + name )
        try2 = [ i for i in try2 if not '/model[0]/plots[0]' in i.path ]  
        if len( try1 ) + len( try2 ) > 1:
            raise SimError( "findObj: ambiguous name: '{}'".format(name) )
        if len( try1 ) + len( try2 ) == 0:
            if noRaise:
                return moose.element('/')
            else:
                raise SimError( "findObj: No object found on '{}' named: '{}'".format( rootpath, name) )
        if len( try1 ) == 1:
            return try1[0]
        else:
            return try2[0]


    def _scaleOneParam( self, params ):
        #print( "scaleOneParam: ", params )
        if len(params) != 3:
            raise SimError( "scaleOneParam: expecting [obj, field, scale], got: '{}'".format( params ) )

        if not params[0] in self.modelLookup:
            foundObj = self.findObj( params[0] )
            if foundObj.name == '/':
                if not self.silent:
                    print( "simWrapMOOSE::_scaleOneParam( {}.{} ) not found".format( params[0], params[1] ) )
            else:
                self.modelLookup[ params[0] ] = [ foundObj.path ]
                if not self.silent:
                    print( "simWrapMOOSE::_scaleOneParam( {}.{} ): added to map ".format( params[0], params[1] ) )
        objPath = self.lookup( params[0] )[0]
        if objPath == '/':  # No object found
            return
        obj =  moose.element( objPath )
        if obj.path == '/': # No object found on path
            return
        field = params[1]
        scale = float( params[2] ) # This is now the assignment value.
        if not isinstance(field,str):
            field = field.decode()
        else:
            field = field
        if not ( scale >= 0.0):
            raise SimError( "Error: Scale {} out of range".format( scale ) )

        if field == 'Kd':
            setReacKd( obj, scale )
        elif field == 'tau':
            setReacTau( obj, scale )
        else: 
            val = obj.getField( field )
            obj.setField( field, scale)
            #print("ScaledParam {} {}.{} from {} to {} with scale {}".format( obj.path, params[0], field, val, obj.getField( field ), scale ) )
        return

    def deleteItems( self, itemsToDelete ):
        for ( entity, change ) in itemsToDelete[:]:
            entity = entity.strip(' \n\t\r')
            if entity in self.modelLookup:
                objPathList = self.modelLookup[entity]
                for objPath in objPathList:
                    if (self.ignoreMissingObj and objPath == '/') :
                        if self.silent == False:
                            print( "Alert: simWrapMoose::deleteItems: Object in entity list but not in model '{}'".format( entity ) )
                        continue
                    if change == 'delete':
                        if objPath != self.modelId.path and moose.exists( objPath ):
                            moose.delete( objPath )
                        else:
                            raise SimError("Cannot delete modelId or rootPath: '{}'".format( objPath) )
            elif self.silent == False:
                print( "Alert: simWrapMoose::deleteItems: '{}' not found".format( entity ) )


    def subsetItems( self, modelSubset ):
        origNumSubs = {} # Key is path of obj, val is [nsub, nprd]
        directContainers = []
        indirectContainers = [self.modelId]
        nonContainerSet = set()
        doomed = set()

        kinpath = self.modelId.path
        '''
        for e in moose.wildcardFind( "{0}/##[ISA=EnzBase],{0}/##[ISA=Reac]".format(kinpath) ):
            origNumSubs[e.path] = [len( e.neighbors['sub'] ), len( e.neighbors['prd'] ) ]
        '''
        allIn = set()
        for i in modelSubset: 
            allIn.update( self.lookup( i ) )

        for i in modelSubset: 
            elist = self.lookup( i )
            #print( "SUBSETTING: ", i, elist, self.ignoreMissingObj )
            for elmPath in elist:
                if self.ignoreMissingObj and elmPath == '/':
                    continue
                elm = moose.element( elmPath )
                if elm.path == '/':
                    continue
                #print( "elmpath = ", elmPath )

                if isContainer(elm):
                    indirectContainers.extend( getContainerTree(elm, kinpath))
                    directContainers.append(elm)
                    # I need to ensure that none of the children of 
                    # included groups are deleted by another included group.
                    linkSet, dropSet = findLinkSet( elmPath, allIn )
                    #print( "LinkSet = ", linkSet )
                    #print( "DropSet = ", dropSet )
                    nonContainerSet.update( linkSet )
                    doomed.update( dropSet )
                else:
                    indirectContainers.extend( getContainerTree(elm, kinpath))
                    nonContainerSet.add( elm.path )

        # Eliminate indirectContainers that are descended from a
        # directContainer: all descendants of a direct are included
        dirset = set( [i.path for i in directContainers] )
        indirectContainers = [ i for i in indirectContainers if isNotDescendant( i, dirset ) ]

        # Make the containers unique. Put in a set.
        inset = set( [i.path for i in indirectContainers] )
        #nonset = set( [i.path for i in nonContainers] )

        #print( "INSET = ", inset, ", nonset = ", nonContainerSet )

        # Go through all immediate children of indirectContainers, 
        #   and mark for deletion in doomedList
        for i in inset:
            doomed.update( [j.path for j in moose.wildcardFind( i + '/#[]' ) ] )
        # Remove nonContainers, IndrectContainers and DirectContainers
        #   from doomedList
        doomed = ((doomed - inset) - dirset) - nonContainerSet

        # Delete everything in doomedList
        for i in doomed:
            if moose.exists( i ):
                #print( i )
                moose.delete( i )
            elif not self.silent:
                print( "Warning: deleting doomed obj {}: it does not exist".format( i ) )
        # Remove all enzymes which have changed substrates or products.
        '''
        for e in moose.wildcardFind( "{0}/##[ISA=EnzBase],{0}/##[ISA=Reac]".format(kinpath) ):
            if origNumSubs[ e.path ] != [len(e.neighbors['sub']), len( e.neighbors['prd'] ) ]:
                moose.delete( e )
        '''

    def changeParams( self, parameterChange ):
        for (entity, field, value) in parameterChange:
            if len( self.lookup(entity) ) == 0:
                continue
            objPath = self.lookup( entity )[0]
            if objPath == '/':
                continue
            if field == "concInit (uM)":
                field = "concInit"
            obj = moose.element( objPath )
            if obj.path == '/':
                continue
            obj.setField( str( field ), value )
            #print( "PARAM {}.{} = {}, buf = {}".format( obj.name, field, value, obj.isBuffered ) )

    def buildModelLookup( self, tempModelLookup ):
        for key, paths in tempModelLookup.items():
            foundObj = [ self.findObj( p, noRaise = True ) for p in paths ]
            foundObj = [ j.path for j in foundObj if j.name != '/' ]
            if len( foundObj ) > 0:
                self.modelLookup[key] = foundObj

    def loadModelFile( self, fname, modifyFunc, scaleParam, dumpFname, paramFname ): # modify arg is a func
    #This list holds the entire models Reac/Enz sub/prd list for reference
        if moose.exists( '/model' ):
            raise SimError( "loadModelFile: Model already exists" )
        erSPlist = {}
        fileName, file_extension = os.path.splitext( fname )
        if file_extension == '.xml':
            self.modelId, errormsg = moose.readSBML( fname, 'model', 'ee' )
        elif file_extension == '.g':
            self.modelId = moose.loadModel( fname, 'model', 'ee' )
        # moose.delete('/model[0]/kinetics[0]/compartment_1[0]')
        elif file_extension == '.py':
            # Assume a moose script for creating the model in rdesigneur.
            # It must have a function load() which returns the rdes object.
            # The load() function creates rdes and its prototypes.
            # It must have a function build( rdes) which completes the
            # model.
            # Following the load() command, the chemical system for the 
            # model must live under
            #       /library/chem
            spec = util.spec_from_file_location("mscript", fname )
            mscript = util.module_from_spec(spec)
            spec.loader.exec_module(mscript)
            rdes = mscript.load()
            '''
            # Deprecated Python syntax from pre 3.3
            mscript = imp.load_source( "mscript", fname )
            rdes = mscript.load()
            '''
            if not moose.exists( '/library/chem' ):
                if ( moose.exists( '/library/cell' ) ):
                    self.modelId = moose.element( '/library/cell' )
                else: 
                    self.modelId = moose.Neutral( '/library/chem' )
            else:
                self.modelId = moose.element( '/library/chem' )
        self.buildModelLookup( self.objMap )
        mpath = self.modelId.path
        for f in moose.wildcardFind('{0}/##[ISA=Reac],{0}/##[ISA=EnzBase]'.format( mpath ) ):
            erSPlist[f] = {'s':len(f.neighbors['sub']), 'p':len(f.neighbors['prd'])}
        # Then we apply whatever modifications are specified by user or protocol
        
        modelWarning = ""
        # We have to scale params _before_ modifying the model since the
        # expt modifications override anything done to the model params.
        self._scaleParams( scaleParam )
        if modifyFunc != None:
            modifyFunc( erSPlist, modelWarning )
        self.turnOffElec = False
        if file_extension == ".py":
            # Deprecated. Here we override the rdes to NOT make a solver.
            #self.turnOffElec = rdes.turnOffElec
            #rdes.turnOffElec = False
            #print( "LIB: ", moose.element( '/library/chem/kinetics/glu/vesicle_release' ).Kf )
            mscript.build( rdes )
            #print( "MODEL: ", moose.element( '/model/chem/dend/glu/vesicle_release' ).Kf )
            self.modelId = moose.element( '/model' )
            self.buildModelLookup( self.objMap )
            #rdes.turnOffElec = self.turnOffElec
            moose.reinit()
        if len(dumpFname) > 2:
            if dumpFname[-2:] == '.g':
                moose.writeKkit( self.modelId.path, dumpFname )
            elif len(dumpFname) > 4 and dumpFname[-4:] == '.xml':
                moose.writeSBML( self.modelId.path, dumpFname )
            else:
                raise SimError( "Subset file type not known for '{}'".format( dumpFname ) )

        if len(paramFname) > 0:
            generateParamFile( self.modelId.path, paramFname )
            quit()

        # Now we have finished doing tweaking, redefine the modelId
        self.modelId = moose.element( '/model' )


    def buildSolver( self, solver, useVclamp = False, minInterval = 1.0 ):
        # Here we remove and rebuild the HSolver because we have to add vclamp
        # after loading the model.
        if useVclamp: 
            self.turnOffElec = False
            if moose.exists( '/model/elec/hsolve' ):
                raise SimError( "Hsolve already created. Please rebuild \
                        model without HSolve." )
    
        if (not self.turnOffElec) and moose.exists( '/model/elec/soma' ) and not moose.exists( '/model/elec/hsolve' ):
            for i in range( 9 ):
                moose.setClock( i, elecDt )
            moose.setClock( 8, elecPlotDt )
            tgt = '/model/elec/soma'
            hsolve = moose.HSolve( '/model/elec/hsolve' )
            hsolve.dt = elecDt
            hsolve.target = tgt
            moose.reinit()
    
        compts = moose.wildcardFind( self.modelId.path + '/##[ISA=ChemCompt]' )
        for compt in compts:
            if solver.lower() in ['none','ee','exponential euler method (ee)']:
                return
            if len( moose.wildcardFind( compt.path + "/##[ISA=Stoich]" ) ) > 0:
                #print( "findSim::buildSolver: Warning: Chem solvers already defined. Use 'none' or 'ee' in solver specifier to avoid this message. Model should work anyway." )
                return
            if solver.lower() in ['gssa','stochastic simulation (gssa)']:
                ksolve = moose.Gsolve ( compt.path + '/gsolve' )
            elif solver.lower() in ['gsl','runge kutta method (gsl)']:
                ksolve = moose.Ksolve( compt.path + '/ksolve' )
            elif solver.lower() in ['lsoda']:
                ksolve = moose.Ksolve( compt.path + '/ksolve' )
                ksolve.method = 'lsoda'
            stoich = moose.Stoich( compt.path + '/stoich' )
            stoich.compartment = moose.element( compt.path )
            stoich.ksolve = ksolve
            stoich.reacSystemPath = compt.path + '/##'
            for i in range( 10, 20 ):
                moose.setClock( i, 0.5 * minInterval )

    def buildVclamp( self, stim ):
        # Stim.entities should be the compartment name here.
        comptPath = self.lookup( stim.entities[0] )[0]
        vclamp = moose.VClamp( comptPath + '/vclamp' )
        self.modelLookup['vclamp'] = [vclamp.path,]
        compt = moose.element(comptPath)
        vclamp.mode = 0     # Default. could try 1, 2 as well
        vclamp.tau = 0.2e-3 # lowpass filter for command voltage input
        vclamp.ti = 20e-6   # Integral time
        vclamp.td = 5e-6    # Differential time. Should it be >= dt?
        vclamp.gain = compt.Cm * 5e3  
        # assume SI units. Scaled by area so that gain is reasonable. 
        # Needed to avert NaNs.

        # Connect voltage clamp circuitry
        moose.connect( compt, 'VmOut', vclamp, 'sensedIn' )
        moose.connect( vclamp, 'currentOut', compt, 'injectMsg' )
        moose.reinit()
        return vclamp.path
    

    def pruneDanglingObj( self, erSPlist):
        kinpath = self.modelId.path
        erlist = moose.wildcardFind(kinpath+"/##[ISA=Reac],"+kinpath+ "/##[ISA=EnzBase]")
        subprdNotfound = False
        ratelawchanged = False
        funcIPchanged  = False
        toDelete = []
        mWarning = ""
        mRateLaw = ""
        mFunc = ""
        for i in erlist:
            isub = i.neighbors["sub"]
            iprd = i.neighbors["prd"]
            tobedelete = False
            if moose.exists(i.path):
                if len(isub) == 0 or len(iprd) == 0 :
                    subprdNotfound = True
                    mWarning = mWarning+"\n"+i.className + " "+i.path
                    moose.delete( i )
                elif len(isub) != erSPlist[i]["s"] or len(iprd) != erSPlist[i]["p"]:
                    ratelawchanged = True
                    mRateLaw = mRateLaw+"\n"+i.path
                    moose.delete( i )
                    
        flist = moose.wildcardFind( kinpath + "/##[ISA=Function]" )
        for i in flist:
            if len(i.neighbors['valueOut']) == 0:
                moose.delete(moose.element(i))
            if len(moose.element(moose.element(i).path+'/x').neighbors['input']) == 0 or  \
                len(moose.element(moose.element(i).path+'/x').neighbors['input']) != i.numVars:
                funcIPchanged = True
                #print( "In {0}, numVars = {1}".format( i.path, i.numVars) )
                mFunc = mFunc+"\n"+i.path
    
        if subprdNotfound:
            if not self.silent:
                print(" \nWarning: Found dangling Reaction/Enzyme, Automatically deleted. {} ".format( mWarning) )
        if ratelawchanged:
            if not self.silent:
                print("\nWarning: This reaction or enzyme's RateLaw needs to be corrected as its substrate or product were deleted while subsetting. Program will continue. \n"+mRateLaw)
        if funcIPchanged:
            raise SimError ("\nError while subsetting: one or more inputs to function '{}' are missing. If function needs to be deleted  then add it to the worksheet in ModelMapping -> itemstodelete section. Else restore the missing molecules. Program will exit now.\n".format( mFunc ) )
        
    def setHsolveState(self, state, pauseHsolve ):
        if moose.exists( '/model/elec/hsolve' ):
            if state:
                for i in range( 9 ):
                    moose.setClock( i, pauseHsolve.elecDt )
            else:
                for i in range( 9 ):
                    moose.setClock( i, 1e12 )
            moose.setClock( 8, pauseHsolve.elecPlotDt )
            
    def cellLongAxis( self, compts ):
        if len( compts ) < 2:
            return np.array( [1.0,0.0,0.0] )
        L = np.zeros(3)
        soma = moose.wildcardFind( '/model/elec/#soma#' )
        if len( soma ) < 1:
            s = np.zeros(3)
        else:
            s = np.array( [soma[0].x, soma[0].y, soma[0].z] )
        for i in compts:
            L[0] += i.x
            L[1] += i.y
            L[2] += i.z
        L -= s * len(compts)
        return L/np.sqrt( sum( [x*x for x in L] ) )

    def makeReadoutPlots( self, readouts ):
        moose.Neutral('/model/plots')
        self.numMainPlots = 0
        for i in readouts:
            readoutElmPaths = []
            for j in i.entities:
                readoutElmPaths.extend( self.lookup(j) )
            for elmPath in readoutElmPaths:
                ######Creating tables for plotting for full run #############
                if elmPath == '/' or not moose.exists( elmPath ):
                    continue
                self.numMainPlots += not( i.isPlotOnly )
                elm = moose.element( elmPath )
                plotpath = '/model/plots/' + ntpath.basename(elm.name)
                if i.field in i.elecFields:
                    plot = moose.Table(plotpath)
                elif i.field in i.fepspFields:
                    numCompts = moose.element( '/model/elec' ).numCompartments
                    plot = moose.Table(plotpath, numCompts )
                else:
                    plot = moose.Table2(plotpath)
                self.plotPath[elm.path] = plotpath
                #i.plots[elm.name] = plot
                if i.field in i.epspFields:   # Do EPSP stuff.
                    fieldname = 'getVm'
                    #i.epspPlot = plot
                elif i.field in i.fepspFields:   # Do fEPSP stuff.
                    fieldname = 'getIm'
                    #i.epspPlot = plot
                    i.wts = []
                    pv = plot.vec
                    idx = 0
                    compts = moose.wildcardFind( '/model/elec/##[ISA=CompartmentBase]' )
                    L = self.cellLongAxis( compts )
                    for k,p in zip( compts, pv ):
                        moose.connect( p, 'requestOut', k, fieldname )
                        # We do not know ahead of time what the orientation of
                        # the cell is. 
                        # Assume a cell long axis vector L. 
                        # Assume integration is in the plane orthogonal to r.
                        # Assume soma roughly at 0,0,0
                        dy = np.dot( L, [k.x-i.ex, k.y-i.ey, k.z-i.ez] )
    
                        #dx = k.x-i.ex
                        #dy = k.y-i.ey
                        #dz = k.z-i.ez
                        # This is the wrong, but easy version
                        #r = np.sqrt( dx*dx + dy*dy + dz*dz )
                        #i.wts.append( fepspScale/r )
                        #
                        # Here is the correct version, integrating over the
                        # pyramidal cell layer.
                        ret = fepspInteg(i.fepspMax, dy) - \
                            fepspInteg(i.fepspMin, dy)
                        i.wts.append( ret * fepspScale )
                    return
                elif i.field in i.epscFields:   # Do EPSC stuff.
                    fieldname = 'getCurrent'
                    '''
                    path = elm.path + '/vclamp'
                    if moose.exists( path ):
                        elm = moose.element( path )
                    else:
                        raise SimError( "makeReadoutPlots: Cannot find vclamp on {}".format( elm.path ) )
                    '''
                    #i.epspPlot = plot
                else:
                    fieldname = 'get' + i.field.title()
                moose.connect( plot, 'requestOut', elm, fieldname )

    def fillPlots( self ):
        plots = []
        dt = []
        for i in self.plotPath.values():
            plotvec = moose.vec( i )
            for j in plotvec:
                plots.append( j.vector ) # should be a numpy array
                dt.append( j.dt )
                #print( "FillPlots: dt = {}, n = {}, dataIndex = {} ".format( dt, len(j.vector), j.index ) )
        return plots, dt,  self.numMainPlots
    
    def deliverStim( self, qe ):
        field = qe.entry.field
        #field = model.fieldLookup[s.field]
        for name in qe.entry.entities:
            if not name in self.modelLookup:
                raise SimError( "simWrapMoose::deliverStim: entity '{}' not found, check object map".format( name ) )
            elmPaths = self.modelLookup[name]
            #print( "deliverStim {}.{}  {}@{}".format( elms[0].path, field, qe.val, moose.element( '/clock' ).currentTime ) )
            for ePath in elmPaths:
                if ePath == '/' or not moose.exists( ePath ):
                    continue

                if field == 'Vclamp':
                    path = ePath + '/vclamp'
                    moose.element( path ).setField( 'command', qe.val )
                    #print(" Setting Vclamp {} to {}".format( path, qe.val ))
                else:
                    e = moose.element( ePath )
                    e.setField( str(field), qe.val )
                    if qe.t == 0:
                        ## At time zero we initial the value concInit or nInit
                        if field == 'conc':
                            e.setField("concInit",qe.val)
                            moose.reinit()
                        elif field == "n":
                            e.setField( 'nInit', qe.val )
                            moose.reinit()

    def getCurrentTime( self ):
        return moose.element( '/clock' ).currentTime

    def advanceSimulation( self, advanceTime, doPlot = True, doSettle = False ):
        moose.start( advanceTime )

    def reinitSimulation( self ):
        moose.reinit()

    def steadyStateStims(self, stimList, responseList, isSeries = False, settleTime = 300 ):
        '''
        Computes steady_state output for specified stimulus combinatations.
        stimList is 2-D list of 
            (stimEntity, field, value, scale) tuples. 
        The first dimension is the combined stimulus for each data point
        The second dimension is the series of data points.
        responseList is list of 
            (respEntityList, field, refEntityList, field) 
        tuples for the readout. The respEntityList/refEntityList specify
        multiple entities whose values should be summed for the response.
        In some cases we have a special global reference stimulus. This
        is just another entry in the stimList.
        isSeries is true if the entries are successive, like a dose-response
        This function is used for a doser by having just the same
        stimulus entity throughout, for a series of doses.
        Returns the list of responses, and the list of matching references.
        '''
        moose.reinit()
        ret = []
        ref = []
        orig = 0.0
        #numElms = len( moose.wildcardFind( '/model/kinetics/##' ) )
        #print( "SteadyStateStims: settleTime = {}, chemDt = {}, isSeries = {}, numElms = {}".format( settleTime, moose.element( '/clock').dts, isSeries, numElms ) )
        if isSeries:
            moose.reinit()
        for pt in stimList:
            if isSeries:
                for (stimEntity, field, value, scale) in pt: 
                    # here we assign the stimulus.
                    #print ("setField {}.{} = {}".format( stimEntity, field, value*scale ) )
                    if not stimEntity in self.modelLookup:
                        raise SimError( "simWrapMoose::deliverStim: entity '{}' not found, check object map".format( stimEntity ) )
                    elmPath = self.modelLookup[stimEntity][0]
                    if not moose.exists( elmPath ):
                        continue
                    elm = moose.element( elmPath )
                    if 'conc' in field:
                        elm.setField( "concInit", value * scale )
                        elm.setField( "conc", value * scale )
                    else:
                        elm.setField( field, value * scale )
                    #print ("setField {}.{} = {}; Buf = {}".format( elm.path, field, value*scale, elm.isBuffered ) )
                moose.start( settleTime )
            else:
                orig = []
                for (stimEntity, field, value, scale) in pt: 
                    #print( "SteadyStateStim {}  {}".format( stimEntity, field ) )
                    # here we assign the stimulus.
                    if not stimEntity in self.modelLookup:
                        raise SimError( "simWrapMoose::deliverStim: entity '{}' not found, check object map".format( stimEntity ) )
                    elmPath = self.modelLookup[stimEntity][0]
                    if elmPath == '/' or not moose.exists( elmPath ):
                        raise SimError( "simWrapMoose::deliverStim: Obj for entity '{}' = '{}' not found, check if it has been deleted".format( stimEntity[0], elmPath ) )
                    elm = moose.element( elmPath )

                    orig.append( (elm, field, elm.getField( field ) ) )
                    elm.setField( field, value * scale )
                moose.reinit()
                moose.start( settleTime )
                for elm, field, oldval in orig: # Put values back.
                    elm.setField( field, oldval )

            ret.append( self.sumFields( responseList[0], responseList[1] ) )
            ref.append( self.sumFields( responseList[2], responseList[3] ) )
        return ret, ref

    def deleteSimulation( self ):
        #moose.delete( self.modelId )
        if moose.exists( '/model' ):
            moose.delete( '/model' )
        if moose.exists( '/library' ):
            moose.delete( '/library' )

    def sumFields( self, entityList, field ):
        tot = 0.0
        for rr in entityList:
            elmPaths = self.lookup( rr )
            for ePath in elmPaths:
                if ePath != '/' and moose.exists( ePath ):
                    e = moose.element( ePath )
                    tot += e.getField( str( field ) )
                    #print (" sumFields rr = {}, val = {}".format( e.name, e.conc ) )
        return tot

    def getObjParam( self, entity, field, isSilent = False ):
        if not entity in self.modelLookup:
            # Try to use the entity name directly, without lookup
            foundObj = self.findObj( entity, noRaise = True )
            if foundObj.name == '/':
                if isSilent:
                    return -2.0
                raise SimError( "SimWrapMoose::getObjParam: Entity {} not found, check Object map".format( entity ) )
            else:
                self.modelLookup[ entity ] = [ foundObj.path ]
        elmPathList = self.lookup(entity)
        #print( "IN GetOBJParam, elmPathList = ", elmPathList )
        if len( elmPathList ) != 1:
            if isSilent:
                return -2.0
            raise SimError( "SimWrapMoose::getObjParam({}): Should only have 1 object, found {} ".format( entity, len( elmPathList ) ) )
        if elmPathList[0] == '/' or not moose.exists( elmPathList[0] ):
            if isSilent:
                return -2.0
            moose.le( '/model[0]/kinetics[0]/MAPK[0]/MAPK_p_p[0]' )
            raise SimError( "SimWrapMoose::getObjParam: elm {} not found, check".format( elmPathList[0] ) )

        elm = moose.element( elmPathList[0] )
        if field == 'Kd':
            return getReacKd( elm )
        elif field == 'tau':
            return getReacTau( elm )
        else:
            return elm.getField( field )



    def presettle( self ):
        t0 = time.time()
        self.reinitSimulation()
        self.advanceSimulation( settleTime )
        w = moose.wildcardFind( sw.modelId.path + "/##[ISA=PoolBase]" )
        ret = {}
        for i in w:
            if not i.isBuffered:
                ret[i.path] = i.n
        self.deleteSimulation()
        print( "Done global settle time {:.2f} in {:.2f} seconds".format( settleTime, time.time()-t0))
        print( "s", end = '' )
        sys.stdout.flush()
        return ret

    def assignPresettle( self, settleDict ):
        for key, value in settleDict.items():
            moose.element( key ).nInit = value

#########################################################################

def generateParamFile( model, fname ):
    with open( fname, "w" ) as fp:
        for i in moose.wildcardFind( model + "/##[ISA=PoolBase]" ):
            conc = i.concInit
            if conc > 0.0:
                objName = getUniqueName( model, i )
                fp.write( "{}   concInit\n".format( objName ) )

        for i in moose.wildcardFind( model + "/##[ISA=Reac]" ):
            Kf = i.Kf
            Kb = i.Kb
            if Kb <= 0.0 and Kf <= 0.0:
                return
            objName = getUniqueName(model, i)
            if Kb <= 0.0:
                fp.write( "{}   Kf\n".format( objName ) )
            elif Kf <= 0.0:
                fp.write( "{}   Kb\n".format( objName ) )
            else:   # Prefer the Kd and tau where possible.
                fp.write( "{}   Kd\n".format( objName ) )
                fp.write( "{}   tau\n".format( objName ) )

        for i in moose.wildcardFind( model + "/##[ISA=EnzBase]" ):
            Km = i.Km
            kcat = i.kcat
            if Km <= 0.0 or kcat <= 0.0:
                return
            objName = getUniqueName(model, i)
            fp.write( "{}   Km\n".format( objName ) )
            fp.write( "{}   kcat\n".format( objName ) )


def getUniqueName( model, obj ):
    path1 = "{}/##/{},{}/{}".format( model, obj.name, model, obj.name )
    wf = moose.wildcardFind( path1 )
    assert( len( wf ) > 0 )
    if len( wf ) == 1:
        return obj.name
    pa = obj.parent.name
    path2 = "{}/##/{}/{},{}/{}/{}".format( model, pa, obj.name, model, pa, obj.name )
    wf = moose.wildcardFind( path2 )
    assert( len( wf ) > 0 )
    if len( wf ) == 1:
        return pa + "/" + obj.name
    grandpa = obj.parent.parent.name
    path3 = "{}/##/{}/{}/{},{}/{}/{}/{}".format( model, grandpa, pa, obj.name, model, grandpa, pa, obj.name )
    wf = moose.wildcardFind( path3 )
    assert( len( wf ) > 0 )
    if len( wf ) == 1:
        return pa + "/" + obj.name
    raise SimError( "getUniqueName: {} and {} non-unique, please rename.".format( wf[0].path, wf[1].path ) )
    return obj.name


def fepspInteg( x, dy ):
    # phi(r, t) = (1/(4pi.sigma) ) * Sum_n_in_1toN( I_n(t) / |r-r_n|
    # Here we assume that the cells are all in a single plane and are
    # nearly at the same Y level, and are vertical sticks.
    # Integ =  1/Y * ( ln|x/Y + sqrt(1+(x/Y)^2)| )
    # where Y is y_compt - yelectrode, and x is x_cell, and we take
    # x_electrode as zero.
    # Problem here with singularities.
    #return 1.0/dy * ln( abs(x/dy + np.sqrt( 1+(x/dy)*(x/dy))))
    # Some recalc, I got rid of the exteranal 1.0/dy
    return np.log( abs(x) + np.sqrt( x*x + dy*dy) )
