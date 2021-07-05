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
#import ntpath
import json
import numpy as np
import moose
#import imp  ## May be deprecated from Python 3.4
from simWrap import SimWrap 
from simError import SimError
import hillTau

SIGSTR = "{:.4g}" # Used for dumping JSON files.

class SimWrapHillTau( SimWrap ):
    def __init__( self, *args, **kwargs ):
        SimWrap.__init__( self, *args, **kwargs )
        self.plotPath = {}
        self.plotDt = 1.0
        self.settleTime = 300.0
        # Inherited from SimWrap: self.modelLookup = {}
        self.model = ""

    def _scaleOneParam( self, params ):
        if len(params) != 3:
            raise SimError( "scaleOneParam: expecting [obj, field, scale], g    ot: '{}'".format( params ) )
        if not params[0] in self.modelLookup:
            if self.silent:
                return
            else:
                print( "simWrapHillTau:scaleOneParam: entity '{}' not known".format( params[0] ) )

        entity = self.modelLookup[ params[0] ][0]
        field = params[1]
        scale = float( params[2] )
        if not ( scale >= 0.0 and scale <= 100.0 ):
            raise SimError( "scaleOneParam: {} out of range 0 to 100".format( scale ) )
        if field in ["conc", "concInit"]:
            mol = self.model.molInfo[ entity ]
            c = self.model.concInit[ mol.index ] * scale 
            self.model.conc[ mol.index ]= self.model.concInit[mol.index]= c
            self.jsonDict["Groups"][mol.grp]["Species"][mol.name] = c
        elif field in ["KA", "tau", "tau2", "baseline", "gain", "Kmod", "Amod"]:
            reac = self.model.reacInfo[ entity ]
            dictReac = self.jsonDict["Groups"][reac.grp]["Reacs"][reac.name]
            if field == "KA":
                reac.KA *= scale
                reac.kh = reac.KA ** reac.HillCoeff
                dictReac["KA"] = reac.KA
                #print( "rescale {}.KA: new = {}, scale = {}".format( reac.name, reac.KA, scale ) )
            elif field == "tau":
                # There is an implicit linkage of tau and tau2 when equal.
                if np.isclose( reac.tau, reac.tau2 ):
                    reac.tau2 = reac.tau * scale
                reac.tau *= scale
                dictReac["tau"] = reac.tau
            elif field == "tau2":
                reac.tau2 *= scale
                dictReac["tau2"] = reac.tau2
            elif field == "baseline":
                reac.baseline *= scale
                #print( "BASELINE = {};     SCALE = {}".format(reac.baseline, scale) )
                dictReac["baseline"] = reac.baseline
            elif field == "gain":
                reac.gain *= scale
                dictReac["gain"] = reac.gain
            elif field == "Kmod":
                reac.Kmod *= scale
                dictReac["Kmod"] = reac.Kmod
            elif field == "Amod":
                reac.Amod *= scale
                dictReac["Amod"] = reac.Amod

    def deleteItems( self, itemsToDelete ):
        # This operates at the level of the JSON dict. We then have to
        # rebuild the model.
        jd = self.jsonDict
        for ( _entity, change ) in itemsToDelete:
            if change != 'delete':
                continue
            _entity = _entity.strip( ' \n\t\r' )
            if _entity == '':
                continue
            objList = self.modelLookup.get( _entity )
            if objList:
                for obj in objList:
                    deleteObj( obj, jd['Groups'] )
            elif self.ignoreMissingObj:
                if not self.silent:
                    print( "Alert: simWrapHillTau::deleteItems: entity '{}' not found".format( _entity ) )
            else:
                raise SimError( "SimWrapHillTau::deleteItems: Entity '{}' not found".format( _entity ) )

    def deleteObj( self, obj, grps ):
            grps = jd['Groups']
            if obj in grps:
                del grps[ obj ]
            else: # Scan through all the groups
                for i in grps:
                    found = False
                    if obj in i["Reacs"]:
                        del i["Reacs"][ obj ]
                        found = True
                    if obj in i["Species"]:
                        # Here we have the tricky situation that there may
                        # be reacs that depend on this species. Fortunately
                        # in the HillTau form, all substrates are created
                        # as species with a conc of zero. So this would
                        # not contribute to any downstream activity
                        del i["Species"][ obj ]
                        found = True
                    if obj in i["Eqns"]:
                        del i["Eqns"][ obj ]
                        found = True
                    if not found:
                        raise SimError( "deleteObj: Obj '{}' not found".format( obj ) )

    def subsetItems( self, _modelSubset ):
        # This saves only those entries specified in the subset.
        # In order to do so, it must save anything closer to the root.
        # For the purposes of HillTau models, it saves the groups above
        # each entry.
        # Also has to save all substrates of each reaction entry.
        # But normally the subset only refers to molecules.
        modelSubset = {}
        for i in _modelSubset:
            if i in self.objMap:
                modelSubset[i] = self.objMap[i]
            elif not self.silent:
                print( "Warning: in subsetItems(): item {} not found".format( i ) )
        '''
        try:
            modelSubset = [ self.modelLookup[i][0] for i in _modelSubset]
        except KeyError as ve:
            raise SimError( "subsetItems: Obj '{}' not known".format( i ) )
        '''

        jd = self.jsonDict
        notSavedGrps = [ i for i in jd["Groups"] if not i in modelSubset ]
        rescue = {}
        #assert( len( savedGrps ) + len( notSavedGrps ) == len( jd["Groups"])
        for g in notSavedGrps: 
            # make copies of objs that should be saved, including their
            # parent groups that have to be rescued.
            # Kill groups that have no saved items
            jg = jd["Groups"][g]
            rescue[ g ] = { "Species": {}, "Reacs": {}, "Eqns" : {} }
            doRescue = False
            if "Species" in jg:
                for mol, val in jg["Species"].items():
                    if mol in modelSubset:
                        rescue[g]["Species"][mol] = val
                        doRescue = True
            if "Reacs" in jg:
                for reac, val in jg["Reacs"].items():
                    if reac in modelSubset:
                        rescue[g]["Reacs"][reac] = val
                        doRescue = True
            if "Eqns" in jg:
                for eqn, val in jg["Eqns"].items():
                    if eqn in modelSubset:
                        rescue[g]["Eqns"][eqn] = val
                        doRescue = True
            #print( "************   Deleting jg: {}".format( g ) )
            del jd["Groups"][g]
            if not doRescue:
                #print( "************   Not rescuing jg: {}".format( g ) )
                del rescue[g]

        # Merge the saved groups with the rescued groups.
        #print( "************   jd[Groups]: {}".format( jd["Groups"] ) )
        jd["Groups"].update( rescue )

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

    def loadModelFile( self, fname, modifyFunc, scaleParam, dumpFname, paramFname ):
        self.turnOffElec = True
        fileName, file_extension = os.path.splitext( fname )
        if file_extension == '.json':
            self.jsonDict = hillTau.loadHillTau( fname )
            qs = hillTau.getQuantityScale( self.jsonDict )
            hillTau.scaleDict( self.jsonDict, qs )
            self.extendObjMap() # Extends objects from jsonDict into objMap
            # It comes back as deleteItems, subsetItems, prune, changeParams
            modifyFunc( {}, "" ) # Callback.
            self.model = hillTau.parseModel( self.jsonDict )
            self.buildModelLookup( self.objMap ) 
            #print( "loadModelFile: scaling parms {}".format( scaleParam ) )
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
            if v in self.model.molInfo or v in self.model.reacInfo or v in self.model.eqnInfo:
                self.modelLookup[key] = val
        '''
        for key, val in self.modelLookup.items():
            print( "modelLookup[{}] = {}".format( key, val ) )
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
                #print( "##########{}".format( objList ) )
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
        self.model.advance( advanceTime, settle = doSettle )
        if doPlot:
            tempArray = np.array(self.model.plotvec[:][j:]).transpose()
            for index, plotNum in self.plotPath.values():
                self.plots[plotNum].extend( tempArray[index] )
        return

    def reinitSimulation( self ):
        self.model.reinit()
        return

    def sumFields( self, entityList, field ):
        tot = 0.0
        for rr in entityList:
            elms = self.modelLookup[rr]
            for e in elms:
                mi = self.model.molInfo[e]
                tot += self.model.conc[ mi.index ]
        return tot

    def setField( self, objName, field, value ):
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

    def getField( self, objName, field ):
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


    def getObjParam( self, entity, field ):
        if not entity in self.modelLookup:
            raise SimError( "SimWrapHillTau::getObjParam: Entity {} not found".format( entity ) )
        elms = self.modelLookup[entity]
        if len( elms ) != 1:
            raise SimError( "SimWrapHillTau::getObjParam: Should only have 1 object, found {} ".format( len( elms ) ) )
        return self.getField( elms[0], field )


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
                        self.setField( elm, "concInit", value * scale )
                self.advanceSimulation( st, doPlot = False, doSettle = True)
                st = settleTime
            else:
                orig = []
                for (stimEntity, field, value, scale) in pt:
                    #print( "BBBBBBBBBBBBBBB {}".format( stimEntity ) )
                    elm = self.modelLookup[ stimEntity ][0]
                    orig.append( ( elm, field, self.getField(elm, field) ) )
                    self.setField( elm, field, value * scale )
                    if field == 'conc':
                        self.setField( elm, "concInit", value * scale )
                self.reinitSimulation()
                self.advanceSimulation( settleTime, doPlot = False )
                for elm, field, oldval in orig:
                    self.setField( elm, field, oldval )
                    if field == 'conc':
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
