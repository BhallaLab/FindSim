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
 * File:            simWrapHillTau.py
 * Description:     HillTau solver for findSim
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/
 '''


from __future__ import print_function
import re
import os
import json
import numpy as np
import moose
from simWrap import SimWrap 
from simError import SimError
import hillTau
import time

SIGSTR = "{:.4g}" # Used for dumping JSON files.

class SimWrapHillTau( SimWrap ):
    def __init__( self, *args, **kwargs ):
        SimWrap.__init__( self, *args, **kwargs )
        self.plotPath = {}
        self.plotDt = 1.0
        self.settleTime = 3000.0    # HillTau settling is indept of time.
        # Inherited from SimWrap: self.modelLookup = {}
        self.model = ""
        self.saveList = []
        self.deleteList = []

    def _scaleOneParam( self, params ):
        if len(params) != 3:
            raise SimError( "scaleOneParam: expecting [obj, field, scale], g    ot: '{}'".format( params ) )
        if params[0] in self.model.namedConsts:
            print( "ERROR: should not be seeing a namedConst in scaleOneParam: ", parms[0] )
            assert( 0 )
            self.model.namedConsts[ params[0] ] = float( params[2] )
            self.jsonDict["Consts"][params[0]] = float( params[2] )
            return

        if not params[0] in self.modelLookup:
            if self.silent:
                return
            else:
                print( "simWrapHillTau:scaleOneParam: entity '{}' not known".format( params[0] ) )

        entity = self.modelLookup[ params[0] ][0]
        field = params[1]
        scale = float( params[2] )
        if not ( scale >= 0.0 ):
            raise SimError( "scaleOneParam: {} below 0".format( scale ) )
        if field in ["conc", "concInit"]:
            mol = self.model.molInfo[ entity ]
            self.model.conc[ mol.index ]= self.model.concInit[mol.index]= scale
            self.jsonDict["Groups"][mol.grp]["Species"][mol.name] = scale
        elif field in ["KA", "tau", "tau2", "baseline", "gain", "Kmod", "Amod"]:
            reac = self.model.reacInfo[ entity ]
            dictReac = self.jsonDict["Groups"][reac.grp]["Reacs"][reac.name]
            if field == "KA":
                reac.KA = scale
                reac.kh = reac.KA ** reac.HillCoeff
                dictReac["KA"] = reac.KA
                #print( "rescale {}.KA: new = {}, scale = {}".format( reac.name, reac.KA, scale ) )
            elif field == "tau":
                # There is an implicit linkage of tau and tau2 when equal.
                tau = scale
                if np.isclose( reac.tau, reac.tau2 ):
                    reac.tau2 = tau
                reac.tau = tau
                dictReac["tau"] = reac.tau
            elif field == "tau2":
                reac.tau2 = scale
                dictReac["tau2"] = reac.tau2
            elif field == "baseline":
                reac.baseline = scale
                #print( "BASELINE = {};     SCALE = {}".format(reac.baseline, scale) )
                dictReac["baseline"] = reac.baseline
            elif field == "gain":
                reac.gain = scale
                dictReac["gain"] = reac.gain
            elif field == "Kmod":
                reac.Kmod = scale
                dictReac["Kmod"] = reac.Kmod
            elif field == "Amod":
                reac.Amod = scale
                dictReac["Amod"] = reac.Amod

    def deleteItems( self, itemsToDelete ):
        # This operates at the level of the JSON dict. We then have to
        # rebuild the model.
        for ( _entity, change ) in itemsToDelete:
            if change != 'delete':
                continue
            _entity = _entity.strip( ' \n\t\r' )
            if _entity == '':
                continue
            objList = self.modelLookup.get( _entity )
            if objList:
                for obj in objList:
                    self.deleteList.append( obj )
            elif self.ignoreMissingObj:
                if not self.silent:
                    print( "Alert: simWrapHillTau::deleteItems: entity '{}' not found".format( _entity ) )
            else:
                raise SimError( "SimWrapHillTau::deleteItems: Entity '{}' not found".format( _entity ) )

    def subsetItems( self, _modelSubset ):
        # This builds up a 'saveList' of items to be preserved for
        # calculation.
        # If a subset entry is a group, save all its reactions and eqns.
        # If a subset entry is a reaction or eqn, save it.
        # Don't need to delete anything, just disable unused reacs.
        self.saveList = []
        for i in _modelSubset:
            objList = self.modelLookup.get(i)
            if objList:
                for obj in objList:
                    self.saveList.append( obj )
            elif i in self.jsonDict["Groups"]:
                # The modifySched func recognizes if i is the parent grp
                self.saveList.append( i ) 
                # Could do recursive stuff here if need groups in groups.

            elif self.ignoreMissingObj:
                if not self.silent:
                    print( "Alert: simWrapHillTau::subsetItems: entity '{}' not found".format( i ) )
            else:
                raise SimError( "SimWrapHillTau::subsetItems: Entity '{}' not found".format( i ) )

    def pruneDanglingObj( self, erSPlist ): # Should be clean already
        return

    def changeParams( self, params ):
        ''' 
        simWrapHillTau::changeParams( self, params )
        This changes param values. Note that it gets called BEFORE
        the modelLookup is built. It operates directly on the json dict.
        '''
        for ( entity, field, value) in params:
            for jg in self.jsonDict["Groups"].values():
                if field == "conc" or field == "concInit":
                    s = jg.get( "Species" )
                    if s and entity in s:
                        s[entity] = value
                        #print("Changing {} of '{}' to {}".format( field, entity, value ) )
                elif field == "isBuffered" and value == 1:
                    r = jg.get( "Reacs" )
                    if r and entity in r:
                        self.deleteList.append( entity )
                    else:
                        e = jg.get( "Eqns" )
                        if e and entity in e:
                            self.deleteList.append( entity )
                    #if len( self.deleteList ) > 0:
                    #    self.model.modifySched( saveList = [], deleteList = self.deleteList )

                elif field in ["KA", "tau", "tau2", "baseline", "gain", "Kmod", "Amod"]: 
                    r = jg.get( "Reacs" )
                    if r and entity in r:
                        if field == "KA":
                            r[entity]["KA"] = value
                        elif field == "tau":
                            r[entity]["tau"] = value
                        elif field == "tau2":
                            r[entity]["tau2"] = value
                        elif field == "baseline":
                            r[entity]["baseline"] = value
                        elif field == "gain":
                            r[entity]["gain"] = value
                        elif field == "Kmod":
                            r[entity]["Kmod"] = value
                        elif field == "Amod":
                            r[entity]["Amod"] = value

    def scaleNamedConsts( self, scaleParam ):
        constDict = self.jsonDict.get( "Constants" )
        if constDict:
            newScaleParam = []
            for i in range( 0, len( scaleParam ), 3 ):
                key = scaleParam[i]
                val = scaleParam[i+2]
                if key in constDict:
                    constDict[key] = val
                    #print( "scaling const ", key, " to ", val )
                else:
                    newScaleParam.append( key )
                    newScaleParam.append( scaleParam[i+1] )
                    newScaleParam.append( val )
            # Reassign scaleParam with the found consts removed.
            return newScaleParam
        else:
            return scaleParam

    def loadModelFile( self, fname, modifyFunc, scaleParam, dumpFname, paramFname ):
        #t0 = time.time()
        #print( "Loading model file ", fname, " with numScale = ", len(scaleParam)  )
        self.turnOffElec = True
        fileName, file_extension = os.path.splitext( fname )
        if file_extension == '.json':
            self.jsonDict = hillTau.loadHillTau( fname )
            scaleParam = self.scaleNamedConsts( scaleParam )
            qs = hillTau.getQuantityScale( self.jsonDict )
            hillTau.scaleDict( self.jsonDict, qs )
            self.extendObjMap() # Extends objects from jsonDict into objMap
            # modifyFunc comes back as deleteItems, subsetItems, prune, changeParams
            self.buildModelLookup( self.objMap ) 
            modifyFunc( {}, "" ) # Callback.
            t0 = time.time()
            self.model = hillTau.parseModel( self.jsonDict )
            #print( "loadModelFile: scaling parms {}".format( scaleParam ) )
            self.model.modifySched( saveList = self.saveList, deleteList = self.deleteList )
            self._scaleParams( scaleParam )
            '''
            for i in range( len( scaleParam ) / 6 ):
                j = i*6
                print( "{:12s}{:12s}{:.3f}  {:.3g}".format( scaleParam[j],scaleParam[j+1], scaleParam[j+2], self.getField( scaleParam[j], scaleParam[j+1] ) * 1000 ), end = "\t" )
                j = i*6 + 3
                print( "{:12s}{:12s}{:.3f}  {:.3g}".format( scaleParam[j],scaleParam[j+1], scaleParam[j+2], self.getField( scaleParam[j], scaleParam[j+1] ) * 1000 ) )
            '''
            if len( dumpFname) > 0:
                # convert back into orig units
                hillTau.scaleDict( self.jsonDict, 1.0 / qs ) 
                with open( dumpFname, 'w') as f:
                    json.dump( self.jsonDict, f, indent = 4)
        else:
            raise SimError( "HillTau models are .json. Type '{}' not known".format( fname ) )
        self.loadtime += time.time() - t0
        return


    def extendObjMap( self ):
        om = self.objMap
        for key, val in self.jsonDict["Groups"].items():
            # Only put in the groups which have not been remapped.
            if not key in om:
                om[key] = [key]
            if "Species" in val:
                for i in val["Species"]:
                    if not i in om:
                        om[i] = [i]
            if "Reacs" in val:
                for i in val["Reacs"]:
                    if not i in om:
                        om[i] = [i]

    def buildModelLookup( self, objMap ):
        # All Mols are keys in modelLookup, plus whatever objMap sets.
        # We ensure that only valid objects are keys.
        for key, val in objMap.items():
            v = val[0]
            self.modelLookup[key] = val

    '''
    def buildModelLookup( self, objMap ):
        # All Mols are keys in modelLookup, plus whatever objMap sets.
        # We ensure that only valid objects are keys.
        for key, val in objMap.items():
            print( "Setting modelLookup: ", key, "  ", val )
            v = val[0]
            if v in self.model.molInfo or v in self.model.reacInfo or v in self.model.eqnInfo:
                self.modelLookup[key] = val
                print( "Setting modelLookup: ", key, "  ", val )
    '''

    def buildSolver( self, solver, useVclamp = False ):
        return

    def buildVclamp( self, stim ):
        return

    def setHsolveState(self, state, pauseHsolve):
        return

    def makeReadoutPlots( self, readouts ):
        numPlots = 0
        for i in readouts:
            for j in i.entities:
                if not j in self.modelLookup:
                    continue
                objList = self.modelLookup[ j ]
                for objName in objList:
                    index = self.model.molInfo[objName].index
                    self.plotPath[objName] = [ index, numPlots ]
                    numPlots += 1
        self.plots = [[]]*numPlots

    def fillPlots( self ): # takes plots from sim and puts the numpy arrays of the plot values from sim into the return. Also returns dt as a float.
        return [ np.array( i ) for i in self.plots], self.plotDt
    
    def deliverStim( self, qe ):
        field = qe.entry.field
        for name in qe.entry.entities:
            if not name in self.modelLookup:
                raise SimError( "SimWrapHillTau::deliverStim: Entity {} not found".format( name ) )
            innerNames = self.modelLookup[name]
            for i in innerNames:
                self.setField( i, field, qe.val )

    def getCurrentTime( self ):
        return self.model.currentTime

    def advanceSimulation( self, advanceTime, doPlot = True, doSettle = False ):
        ct = self.model.currentTime
        j = len( self.model.plotvec )
        t0 = time.time()
        self.model.advance( advanceTime, settle = doSettle )
        self.runtime += time.time() - t0
        if doPlot:
            tempArray = np.array(self.model.plotvec[:][j:]).transpose()
            for index, plotNum in self.plotPath.values():
                self.plots[plotNum].extend( tempArray[index] )
        return

    def reinitSimulation( self ):
        t0 = time.time()
        self.model.reinit()
        self.runtime += time.time() - t0
        return

    def sumFields( self, entityList, field ):
        t0 = time.time()
        tot = 0.0
        for rr in entityList:
            elms = self.modelLookup[rr]
            for e in elms:
                mi = self.model.molInfo[e]
                tot += self.model.conc[ mi.index ]
        self.paramAccessTime += time.time() - t0
        return tot

    def setField( self, objName, field, value ):
        t0 = time.time()
        if field in ['conc', 'concInit']:
            #print( "{}.{} = {}".format( objName, field, value ) )
            if objName in self.model.molInfo:
                if field == 'conc':
                    self.model.conc[ self.model.molInfo[objName].index ]= value
                elif field == 'concInit':
                    self.model.concInit[ self.model.molInfo[objName].index ]= value
            else:
                raise SimError( "SimWrapHillTau::setField: Unknown mol {}".format( objName ) )
        elif field in ['KA', 'tau', 'tau2', 'baseline', 'gain', 'Kmod', 'Amod']:
            if objName in self.model.reacInfo:
                reac = self.model.reacInfo[elm]
            else:
                raise SimError( "SimWrapHillTau::setField: Unknown reac {}".format( objName ) )
            if field == 'KA':
                reac.KA = value
                reac.kh = value ** reac.HillCoeff
            elif field == 'tau':
                reac.tau = value
            elif field == 'tau2':
                reac.tau2 = value
            elif field == 'baseline':
                reac.baseline = value
            elif field == 'gain':
                reac.gain = value
            elif field == 'Kmod':
                reac.Kmod = value
            elif field == 'Amod':
                reac.Amod = value
            else:
                raise SimError( "SimWrapHillTau::setField: Unknown obj.field {}.{}".format( objName, field ) )
        else:
            raise SimError( "SimWrapHillTau::setField: Unknown obj.field {}.{}".format( objName, field ) )
        self.paramAccessTime += time.time() - t0

    def getField( self, objName, field ):
        t0 = time.time()
        if field == 'conc':
            if objName in self.model.molInfo: 
                return self.model.conc[ self.model.molInfo[objName].index ]
        if field == 'concInit': 
            if objName in self.model.molInfo:
                #print( "CONCINIT = {}".format( self.model.concInit[ self.model.molInfo[objName].index ] ) )
                return self.model.concInit[ self.model.molInfo[objName].index ]
        elif field in ['KA', 'tau', 'tau2', 'baseline', 'gain', 'Kmod', 'Amod']:
            if objName in self.model.reacInfo: 
                reac = self.model.reacInfo[objName]
            else: 
                raise SimError( "SimWrapHillTau::getField: Unknown reac {}".format( objName ) )
            if field == 'KA':
                return reac.KA
            elif field == 'tau':
                return reac.tau
            elif field == 'tau2':
                return reac.tau2
            elif field == 'baseline':
                return reac.baseline
            elif field == 'gain':
                return reac.gain
            elif field == 'Kmod':
                return reac.Kmod
            elif field == 'Amod':
                return reac.Amod
            else:
                raise SimError( "SimWrapHillTau::setField: Unknown obj.field {}.{}".format( objName, field ) )
        else:
            raise SimError( "SimWrapHillTau::getField: Unknown obj.field {}.{}".format( objName, field ) )
        self.paramAccessTime += time.time() - t0


    def getObjParam( self, entity, field ):
        if entity in self.model.namedConsts:
            return self.model.namedConsts[entity]
        if not entity in self.modelLookup:
            if self.ignoreMissingObj:
                return 1.0
            raise SimError( "SimWrapHillTau::getObjParam: Entity {} not found".format( entity ) )
        elms = self.modelLookup[entity]
        if len( elms ) != 1:
            raise SimError( "SimWrapHillTau::getObjParam: Should only have 1 object, found {} ".format( len( elms ) ) )
        return self.getField( elms[0], field )


    def steadyStateStims(self, stimList, responseList, isSeries = False, settleTime = 3000.0 ):
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
        ret = []
        ref = []
        self.reinitSimulation()
        st = settleTime * 5.0 # The first settle time typically needs to be longer.
        for pt in stimList:
            if isSeries:
                for (stimEntity, field, value, scale) in pt:
                    elm = self.modelLookup[ stimEntity ][0]
                    #print( "SF: {}\t{}\t{}\t{}".format( elm, field, value, scale) )
                    self.setField( elm, field, value * scale )
                    if field == 'conc':
                        self.setField( elm, "conc", value * scale )
                        self.setField( elm, "concInit", value * scale )
                        #self.advanceSimulation( st * 10, doPlot = False, doSettle = True)
                        #print( elm, " conc = ", self.getField( elm, "conc" ) )
                self.advanceSimulation( st * 10, doPlot = False, doSettle = True)
                st = settleTime
            else:
                orig = []
                for (stimEntity, field, value, scale) in pt:
                    elm = self.modelLookup[ stimEntity ][0]
                    orig.append( ( elm, field, self.getField(elm, field) ) )
                    self.setField( elm, field, value * scale )
                    if field == 'conc':
                        self.setField( elm, "conc", value * scale )
                        self.setField( elm, "concInit", value * scale )
                self.reinitSimulation()
                self.advanceSimulation( settleTime, doPlot = False )
                for elm, field, oldval in orig:
                    self.setField( elm, field, oldval )
                    if field == 'conc':
                        self.setField( elm, "conc", oldval )
                        self.setField( elm, "concInit", oldval )

            ret.append( self.sumFields( responseList[0], responseList[1] ) )
            ref.append( self.sumFields( responseList[2], responseList[3] ) )
        return ret, ref
        
    def deleteSimulation( self ):
        self.modelLookup = {}
        self.jsonDict = ""
        self.model = ""
        return

    def presettle( self ):
        return {}

    def assignPresettle( self, settledict ):
        return
