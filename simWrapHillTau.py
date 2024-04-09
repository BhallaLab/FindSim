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
from datetime import datetime

# from simWrap import SimWrap 
# from simError import SimError
# import hillTau
import time

if __package__ is None or __package__ == '':
    from simError import SimError
    from simWrap import SimWrap
    import hillTau
else:
    from FindSim.simError import SimError
    from FindSim.simWrap import SimWrap
    import hilltau as hillTau
    
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
            mol = self.model.molInfo.get( entity )
            if not mol:
                if self.silent:
                    return
                else:
                    raise SimError( "scaleOneParam: Unknown mol: " + entity)
            #mol = self.model.molInfo[ entity ]
            self.model.conc[ mol.index ]= self.model.concInit[mol.index]= scale
            self.jsonDict["Groups"][mol.grp]["Species"][mol.name] = scale
        elif field in ["KA", "tau", "tau2", "baseline", "gain", "Kmod", "Amod"]:
            reac = self.model.reacInfo.get( entity )
            if not reac:
                if self.silent:
                    return
                else:
                    raise SimError( "scaleOneParam: Unknown reac: "+entity)
            #reac = self.model.reacInfo[ entity ]
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
        self.setupModifyDict()
        # This accumulates a list of objects to delete, which is then
        # applied to the model once it is built.
        # Note that we silently ignore requests to delete nonexistent 
        # objects, or objects that are missing from the map.
        # Logic is that if the object doesn't exist here, it doesn't matter
        # if the experiment wants to delete it for some other model.
        deleteSet = set()
        for ( _entity, change ) in itemsToDelete:
            if change != 'delete':
                continue
            _entity = _entity.strip( ' \n\t\r' )
            if _entity == '':
                continue
            objList = self.modelLookup.get( _entity )
            if objList:
                for obj in objList:
                    deleteSet.add( obj )
                    #self.deleteList.append( obj )
            else:
                if not self.silent:
                    print( "Alert: simWrapHillTau::deleteItems: entity '{}' not found".format( _entity ) )
        groups = self.modifiedModelDict["Groups"]
        # Delete the groups first and then come back for the inner objs.
        # Those are less common but messy to find.
        for dd in deleteSet:
            ret = groups.pop( dd, None )
            if ret != None:
                deleteSet.discard( dd )
        for dd in set(deleteSet):    # Now look for inner objects
            ret = self.deleteObjFromModel( groups, dd )
            if ret != None:
                deleteSet.discard( dd )

    def deleteObjFromModel(self, groups, dd ):
        for gg in groups.values():
            rr = gg.get( "Reacs" )
            if rr and dd in rr:
                return rr.pop( dd, None )
            ss = gg.get( "Species" )
            if ss and dd in ss:
                return ss.pop( dd, None )
            ee = gg.get( "Eqns" )
            if ee and dd in ee:
                return ee.pop( dd, None )
        return None

    def findGroupOfObj( groups, obj ):
        if obj in groups:
            return obj
        for gg in groups.values():
            rr = gg.get( "Reacs" )
            if rr and obj in rr:
                return gg
            ss = gg.get( "Species" )
            if ss and obj in ss:
                return ss.pop( obj, None )
            ee = gg.get( "Eqns" )
            if ee and obj in ee:
                return ee.pop( obj, None )
        return None

    def extObjLinkedToGroup( self, grp ):
        # Build up set of species within group
        groupVal = self.modifiedModelDict['Groups'][grp]
        consts = self.modifiedModelDict.get( 'Constants' )
        if consts == None:
            consts = {}
        mySpecies = set()
        if groupVal.get( 'Species' ):
            for ss in groupVal['Species']:
                mySpecies.add( ss )
        if groupVal.get( 'Eqns' ):
            for ee in groupVal['Eqns']:
                mySpecies.add( ee )
        if groupVal.get( 'Reacs' ):
            for rr in groupVal['Reacs']:
                mySpecies.add( rr )

        #print( "MY SPECIES = ",  mySpecies )
        # Scan for reagent species of eqns and reacs, add if outside group.
        ret = set()
        if groupVal.get( 'Eqns' ):
            for eqnName, eqnVal in groupVal['Eqns'].items():
                subs, cs = hillTau.extractSubs( eqnVal, consts )
                for ss in subs:
                    if ss not in mySpecies:
                        ret.add( ss )
        if groupVal.get( 'Reacs' ):
            for rname, rval in groupVal['Reacs'].items():
                for ss in rval['subs']:
                    if ss not in mySpecies:
                        ret.add( ss )
        #print( grp, "NUM Ext Obj= ", len( ret ) )
        return ret

    def allObjLinkedToObj( self, obj ):
        ret = self.findDictOfObj( obj )
        if ret[1] == 'Species':
            return []
        elif ret[1] == 'Eqns':
            return [] # Should parse the equation to extract objects
        elif ret[1] == 'Reacs':
            return ret[3]['subs']

    def findDictOfObj( self, obj ):
        groups = self.modifiedModelDict["Groups"]
        for gg, gval in groups.items():
            for objType, tval in gval.items():
                if objType == "comment":
                    continue
                val = tval.get( obj )
                if val != None:
                    return [ gg, objType, obj, val ]
        print( "Error: Unable to find dict of specified object '{}'. Did you delete it in the experiment file?".format( obj ) )
        assert( 0 )



    def subsetItems( self, _modelSubset ):
        # This builds up a 'saveList' of items to be preserved for
        # calculation.
        # If a subset entry is a group, save all its reactions and eqns.
        # If a subset entry is a reaction or eqn, save it.
        # If a subset doesn't exist in the model, ignore the request
        # without raising an error.
        # Flag all external connections to reacs and Eqns and save them too
        # The reasoning is that the subsetted object is implicitly there,
        # so it is safe as long as we don't try to assign anything to it.
        # If we try to use it as a stim or readout other functions will
        # flag it.
        if len( _modelSubset ) == 0:
            return  # Do not further modify modifiedModelDict
        groups = self.modifiedModelDict["Groups"]
        subsetDict = dict( self.modifiedModelDict )
        subsetDict.pop("Groups", None )
        gdict = {}
        extObjects = set()
        #extEntries = set()
        extEntries = []
        subsettedGroups = set()
        subsettedObjects = set()

        # First pass: collate all groups and objs explicitly listed.
        for i in _modelSubset:
            objList = self.modelLookup.get(i)
            if objList:
                for obj in objList:
                    if obj in groups:
                        subsettedGroups.add( obj )
                    else:
                        subsettedObjects.add( obj )
        # Add reagents to list if they are outside the current subset.
        for gg in subsettedGroups:
            extObjects.update( self.extObjLinkedToGroup( gg ) )
        # Assume all subsetted objects are to be treated as Reacs/Eqns
        # first, and as species only if they are neither.
        # Add all input reagents linked to any subsetted object.
        # This returns an empty list if the object itself is a species.
        for oo in subsettedObjects:
            extObjects.update( self.allObjLinkedToObj( oo ) )
        # Now fill in the extGroups. These have to be reconstructed,
        # not copied wholesale from the source groups dict.
        for oo in extObjects:
            #[grp, objType, objName, objVal] = findDictOfObj( oo )
            entry = self.findDictOfObj( oo )
            if not entry[0] in subsettedGroups:
                extEntries.append( entry )

        # Now we have all the lists. Now march through and rebuild
        # Here are the entire subsetted groups, just copied over.
        for gg in subsettedGroups:
            gdict[gg] = groups[gg]

        # Here are the specific objects to put in the groups.
        for [grp, objType, objName, objVal] in extEntries:
            if not grp in gdict:
                gdict[grp] = {}
            if not "Species" in gdict[grp]:
                gdict[grp]["Species"] = {}
            if objType == "Species":
                gdict[grp][objType][objName] = objVal
            if objType == "Reacs":
                baseline = objVal.get( "baseline" )
                if not baseline:
                    baseline = 0.0
                gdict[grp]["Species"][objName] = baseline
            if objType == "Eqns":
                gdict[grp]["Species"][objName] = 0.0

        # Finally, wrap it up
        subsetDict['Groups'] = gdict
        self.modifiedModelDict = subsetDict


    def pruneDanglingObj( self, erSPlist ): # Should be clean already
        return

    def changeParams( self, params ):
        ''' 
        simWrapHillTau::changeParams( self, params )
        This changes param values. 
        It operates directly on the json dict.
        It is meant to be called AFTER the modelLookup is built. It needs
        to look up and convert names from the expt file to the model Json.
        It does some nasty things for assignments to eqns, which only
        permit string assignments in the hillTau schema.
        If the modified object doesn't exist in the model, raise an error.
        '''
        for ( exptEntity, field, value) in params:
            mm = self.modelLookup.get( exptEntity )
            if not mm:
                raise SimError( "SimWrapHillTau::changeParams: '{}' not found on lookup.".format( exptEntity ) )
            entity = mm[0]
            #print( "changing entity {} to {}.{}={}".format( exptEntity, entity, field, value ) )
            for jg in self.jsonDict["Groups"].values():
                if field == "conc" or field == "concInit":
                    #print("Trying {} of '{}' to {}".format( field, entity, value ) )
                    rr = jg.get( "Reacs" )
                    if rr and entity in rr:
                        rr[entity]["concInit"] = value
                        #print("Changing reac {} of '{}' to {}".format( field, entity, value ) )
                        continue
                    ss = jg.get( "Species" )
                    if ss and entity in ss:
                        ss[entity] = value
                        #print("Changing species {} of '{}' to {}".format( field, entity, value ) )
                        continue
                    ee = jg.get( "Eqns" )
                    if ee and entity in ee:
                        ee[entity] = "concInit=" + str( value )
                        #print("Changing eqn {} of '{}' to {}".format( field, entity, ee[entity] ) )
                        continue
                elif field == "isBuffered" and value == 1:
                    r = jg.get( "Reacs" )
                    if r and entity in r:
                        # This simply removes the entity from the eval queue
                        # self.deleteList.append( entity )
                        r[entity]["isBuffered"] = 1
                        continue
                        #self.setField( entity, "isBuffered",  1 )
                    else:
                        e = jg.get( "Eqns" )
                        if e and entity in e:
                            continue
                            # Ignore it. We assume that if it is buffered then concInit is set or is going to be set.
                            #self.deleteList.append( entity )
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

    def setupModifyDict( self ):
        self.modifiedModelDict = dict( self.jsonDict )
        # Update the Description and Author fields to reflect subsetting.
        description = self.modifiedModelDict.get("Description")
        if not description:
            description = ""
        self.modifiedModelDict["Description"] = description + ": Original model modified by findSim for subset calculations."
        author = self.modifiedModelDict.get("Author")
        if not author:
            author = ""
        self.modifiedModelDict["Author"] = author + ": Programmatic modification by findSim at " + datetime.today().strftime('%Y-%m-%d %H:%M:%S')

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
            # modifyFunc comes back as deleteItems, subsetItems, prune, changeParams
            self.buildModelLookup( self.objMap ) 
            modelWarning = "Warning in subsetting from: " + fname
            if modifyFunc == None:
                self.setupModifyDict()
            else:
                modifyFunc( {}, modelWarning ) # Callback.
            t0 = time.time()
            self.model = hillTau.parseModel( self.jsonDict )
            #print( "loadModelFile: scaling parms {}".format( scaleParam ) )
            #self.model.modifySched( saveList = self.saveList, deleteList = self.deleteList )
            #self.trimModelLookup()
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
                hillTau.scaleDict( self.modifiedModelDict, 1.0 / qs ) 
                with open( dumpFname, 'w') as f:
                    json.dump( self.modifiedModelDict, f, indent = 4)
        else:
            raise SimError( "HillTau models are .json. Type '{}' not known".format( fname ) )
        self.loadtime += time.time() - t0
        return

    def buildModelLookup( self, objMap ):
        # Keys must refer to valid objects
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

    '''
    def trimModelLookup( self ):
        temp = dict( self.modelLookup )
        for key, val in temp.items():
            v = val[0]
            if not( v in self.model.grpInfo or v in self.model.molInfo or v in self.model.reacInfo or v in self.model.eqnInfo ):
                print( " Popping, ", key, val, v )
                self.modelLookup.pop( key )
            if v in self.deleteList:
                print( " Popping-----------, ", key, val, v )
                self.modelLookup.pop( key )
    '''

    def buildSolver( self, solver, useVclamp = False, minInterval = 1 ):
        self.plotDt = minInterval * 0.1
        self.model.dt = minInterval * 0.1
        #print( "Plotdt = {:.3f}, modeldt = {:.3f}, minInterval = {:.3f}".format( self.plotDt, self.model.dt, minInterval ) )
        return

    def buildVclamp( self, stim ):
        return

    def setHsolveState(self, state, pauseHsolve):
        return

    def makeReadoutPlots( self, readouts ):
        numPlots = 0
        self.numMainPlots = 0
        for i in readouts:
            for j in i.entities:
                if not j in self.modelLookup:
                    continue
                objList = self.modelLookup[ j ]
                for objName in objList:
                    index = self.model.molInfo[objName].index
                    self.plotPath[objName] = [ index, numPlots ]
                    numPlots += 1
            if not i.isPlotOnly:
                self.numMainPlots = numPlots
        self.plots = [[]]*numPlots

    def fillPlots( self ): # takes plots from sim and puts the numpy arrays of the plot values from sim into the return. Also returns main plot dt as a float, and the number of main plots.
        tempArray = np.array(self.model.plotvec).transpose()
        for index, plotNum in self.plotPath.values():
            self.plots[plotNum] = tempArray[index]
        return [ np.array( i ) for i in self.plots], [self.plotDt] * len( self.plots ), self.numMainPlots
    
    def deliverStim( self, qe ):
        field = qe.entry.field
        for name in qe.entry.entities:
            #print( "in deliver stim setting {} to {}".format( name, field, qe.val ) )
            if not name in self.modelLookup:
                raise SimError( "SimWrapHillTau::deliverStim: Entity {} not found".format( name ) )
            innerNames = self.modelLookup[name]
            for i in innerNames:
                self.setField( i, field, qe.val )
                if field == "conc":
                    self.setField( i, "concInit", qe.val )

    def getCurrentTime( self ):
        return self.model.currentTime

    def advanceSimulation( self, advanceTime, doPlot = True, doSettle = False ):
        ct = self.model.currentTime
        j = len( self.model.plotvec )
        t0 = time.time()
        self.model.advance( advanceTime, settle = doSettle )
        self.runtime += time.time() - t0
        '''
        if doPlot:
            tempArray = np.array(self.model.plotvec[:][j:]).transpose()
            for index, plotNum in self.plotPath.values():
                self.plots[plotNum].extend( tempArray[index] )
        '''
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
                '''
                idx = self.model.molInfo[objName].index
                self.model.concInit[idx] = self.model.conc[ idx ]= value
                print( "Setting {}[{}] concInit to {}".format( objName, idx, value ) )
                '''
                if field == 'conc':
                    self.model.conc[ self.model.molInfo[objName].index ]= value
                elif field == 'concInit':
                    #print( "Setting {} concInit to {}".format( objName, value ) )
                    self.model.concInit[ self.model.molInfo[objName].index ]= value
            else:
                raise SimError( "SimWrapHillTau::setField: Unknown mol {}".format( objName ) )
        elif field == "isBuffered" and objName in self.model.eqnInfo:
            eqn = self.model.eqnInfo[ objName ]
            eqn.isBuffered = value
        elif field in ['KA', 'tau', 'tau2', 'baseline', 'gain', 'Kmod', 'Amod', "isBuffered"]:
            if objName in self.model.reacInfo:
                reac = self.model.reacInfo[objName]
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
            elif field == 'isBuffered':
                reac.isBuffered = value
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


    def getObjParam( self, entity, field, isSilent = False ):
        if entity in self.model.namedConsts:
            return self.model.namedConsts[entity]
        if not entity in self.modelLookup:
            if self.ignoreMissingObj or isSilent:
                return -2.0
            raise SimError( "SimWrapHillTau::getObjParam: Entity {} not found".format( entity ) )
        elms = self.modelLookup[entity]
        if len( elms ) != 1:
            if isSilent:
                return -2.0
            raise SimError( "SimWrapHillTau::getObjParam({}): Should only have 1 object, found {} ".format( entity, len( elms ) ) )
        if field == "Kd":   # Assume mapping to KA.
            return self.getField( elms[0], "KA" )

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
        #st = settleTime * 5.0 # The first settle time typically needs 
        # to be longer. But I've removed this because it is an unexpected 
        # behaviour and it also leads to numerical issues. I have also 
        # removed a later multiplication of settleTime by 10. If the user
        # wants a long settle time they should assign it explicitly.
        for pt in stimList:
            if isSeries:
                for (stimEntity, field, value, scale) in pt:
                    elm = self.modelLookup[ stimEntity ][0]
                    #print( "SF: {}\t{}\t{}\t{}".format( elm, field, value, scale) )
                    self.setField( elm, field, value * scale )
                    if field == 'conc':
                        self.setField( elm, "conc", value * scale )
                        self.setField( elm, "concInit", value * scale )
                        #print( elm, " conc = ", self.getField( elm, "conc" ) )
                self.advanceSimulation( settleTime, doPlot = False, doSettle = True)
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
