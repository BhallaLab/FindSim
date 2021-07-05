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
 * File:            findSim.py
 * Description:
 * Author:          Upinder S. Bhalla, NishaAnnViswan, HarshaRani
 * E-mail:          bhalla@ncbs.res.in
                    nishaav@ncbs.res.in
                    hrani@ncbs.res.in
 ********************************************************************/

/**********************************************************************
** This program is part of 'MOOSE', the
** Messaging Object Oriented Simulation Environment,
** also known as GENESIS 3 base code.
**           copyright (C) 2003-2021 Upinder S. Bhalla. and NCBS
**********************************************************************/

'''
from __future__ import print_function
import heapq
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import jsonschema
import traceback
import argparse
import os
import re
import time

if sys.version_info < (3, 4):
    import imp               # This is apparently deprecated in Python 3.4 and up
else:
    import importlib      

from simError import SimError
import simWrap
import simWrapMoose
import simWrapHillTau

convertTimeUnits = {'sec': 1.0,'s': 1.0, 
        'ms': 1e-3, 'millisec': 1e-3, 'msec' : 1e-3, 
        'us': 1e-6, 'usec': 1e-6, 'microsec' : 1e-6, 
        'ns': 1e-6, 'nanosec' : 1e-9, 
        'min': 60.0 ,'m' : 60.0, 
        'hours': 3600.0, 'hrs' : 3600.0,
        "days": 86400.0}

convertQuantityUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 
        'nM':1.0e-6, 'pM': 1.0e-9, 'number':1.0, 'ratio':1.0, 
        'V': 1.0, 'mV': 0.001, 'uV': 1.0e-6, 'nV':1.0e-9,
        'A': 1.0, 'mA': 0.001, 'uA': 1.0e-6, 'nA':1.0e-9, 'pA':1.0e-12,
        'Hz': 1.0, '1/sec':1.0, 'sec':1.0, '1/s': 1.0, 's':1.0, 'min':60.0,
        'mV/ms':1.0, '%':100.0, 'Fold change':1.0, 'none': 1 }

defaultScoreFunc = "(expt-sim)*(expt-sim)/(datarange*datarange + 1e-9)"

sw = ""         #default dummy value for SimWrap
fschema = "FindSim-Schema.json" # Name of JSON schema file

def keywordMatches( k, m ):
    return k.lower() == m.lower()

'''
class SimError( Exception ):
    def __init__( self, value ):
        self.value = value
    def __str__( self ):
        return repr( self.value )
'''

##########################################################################

class Experiment:
    """The Experiment class defines the experimental context and source 
    information. It isn't really useful in running the model but is needed
    in the experiement specification file so that we know where the
    data came from, and to look up details."""
    def __init__( self, metadata, expt ):
        self.exptType = expt["design"].lower()
        source = metadata["source"]
        self.exptSource = source.get( "type" )
        self.authors = source.get("authors")
        self.year = source.get( "year" )
        self.citationId = source.get( "PMID" )
        if not self.citationId:
            self.citationId = source.get( "doi" )
        self.journal = source.get( "journal" )
        self.temperature = expt.get( "temperature" )
        self.species = expt.get( "species" )
        self.cellType = expt.get( "cellType" )
        self.testModel = metadata.get( "testModel" )
        self.testMap = metadata.get( "testMap" )

##########################################################################
class Stimulus:
    """Specifies manipulations to be done on a specific component of 
    the model in the course of the simulated experiment. Typically this
    would include adding or removing molecules. Less common might be a
    change in rates (e.g., temperature, or a pharmacological agent that 
    is being modeled as a rate change).
    There can be multiple stimuli during an experiment.
    Dose response is a little special, as here the stimulus only specifies
    the molecule involved. The actual concentrations used are specified in
    the Readout, which contains the dose-response table.
    """
    def __init__( self, s ):
        #self.quantityUnits = s["quantityUnits"].encode( "ascii" ) # Schema ensures it is OK
        self.quantityUnits = s["quantityUnits"] # Schema ensures it is OK
        self.quantityScale = convertQuantityUnits[ self.quantityUnits ]
        self.entities = [s["entity"],]
        self.field = str( s["field"] )
        #self.timeUnits = s.get( "timeUnits" ).encode( "ascii" )
        self.timeUnits = s.get( "timeUnits" )
        if not self.timeUnits:
            self.timeUnits = "s"
        self.timeScale = convertTimeUnits[ self.timeUnits ]
        self.data = s.get( "data" )
        if "label" in s:
            self.label = s["label"]
        else:
            self.label = self.entities[0]

        if not self.data:
            if "value" in s:
                self.data = [[0, s["value"]],]
            else:
                self.data = []

    def load( findsim ):
        ret = []
        fstims = findsim.get( "Stimuli" )
        if fstims:
            for i in fstims:
                ret.append( Stimulus( i ) )
        return ret
    load = staticmethod( load )


    def configure( self, modelLookup ):
        """Sanity check on all fields. First, check that all the entities
        named in experiment have counterparts in the model definition"""
        for i in self.entities:
            #if not i.encode( 'ascii' ) in modelLookup:
            if not i in modelLookup:
                raise SimError( "Stim::configure: Error: object {} not defined in model lookup.".format( i ) )

##########################################################################
# Shifted to Readout class as static fields.
#elecFields = ['Vm', 'Im', 'current'] + epspFields + epscFields
class Readout:
    """Specifies readouts to be obtained from a specific component of 
    the model in the course of the simulated experiment. Almost always
    molecule quantity, but later might be electrical things like membrane 
    potential.
    Currently only a single readout is supported.
    """
    epspFields = [ 'EPSP_peak', 'EPSP_slope', 'IPSP_peak', 'IPSP_slope' ]
    epscFields = [ 'EPSC_peak', 'EPSC_slope', 'IPSC_peak', 'IPSC_slope' ]
    fepspFields = [ 'fEPSP_peak','fEPSP_slope','fIPSP_peak','fIPSP_slope' ]
    postSynFields = fepspFields + epspFields + epscFields
    elecFields = ['Vm', 'Im', 'current'] + epspFields + epscFields
    def __init__( self, ro ):
        self.directParamData = ro.get( "paramdata" )
        if not self.directParamData:
            self.timeUnits = ro["timeUnits"]
            self.timeScale = convertTimeUnits[self.timeUnits]
            self.quantityUnits = ro["quantityUnits"]
            self.quantityScale = convertQuantityUnits[self.quantityUnits]
            self.entities = ro["entities"]
            self.field = ro["field"]
            self.settleTime = ro.get("settleTime")
            if not self.settleTime:
                self.settleTime = 300.0
            self.data = ro.get("data") # For most kinds of data
            if self.data:
                for i in self.data: # force it to have [t, v, sem] in each row
                    if len( i ) == 2:
                        i.append( 0 )
                    assert( len( i ) == 3 )

            self.bardata = ro.get( "bardata" )  # only for barcharts
            self.tabulateOutput = False
            self.normMode = "none"
            norm = ro.get( "normalization" )
            self.useNormalization = False
            self.ratioReferenceEntities = []
            self.ratioReferenceTime = 0
            self.ratioReferenceDose = 0
            self.ratioReferenceValue = 1.0
            if norm:
                self.useNormalization = True
                self.ratioReferenceEntities = norm["entities"]
                #if len( self.ratioReferenceEntities ) > 0 and not self.entities[0] in self.ratioReferenceEntities:
                self.normMode = norm["sampling"]
                if self.normMode == "none":
                    self.useNormalization = False
                elif self.normMode == "start":
                    self.ratioReferenceTime = 0
                elif self.normMode == "presetTime":
                    self.ratioReferenceTime = norm["time"]
                elif self.normMode == "each":
                    self.ratioReferenceTime = -1
                elif self.normMode == "dose":
                    self.ratioReferenceDose = norm["dose"]
                    self.settleTime = ro.get("settleTime")
                    self.ratioReferenceTime = norm.get("time")
                    if not self.ratioReferenceTime:
                        self.ratioReferenceTime = self.settleTime
            # Set up lists to use in the analysis
            self.simData = []
            self.ratioData = []
            self.plots = []
            # Set up Display parameters
            self.useXlog = False
            self.useYlog = False
            self.plotDt = 0.1,
            disp = ro.get( "display" )
            if disp:
                if "useXlog" in disp:
                    self.useXlog = disp["useXlog"]
                if "useYlog" in disp:
                    self.useYlog = disp["useYlog"]
                if "plotDt" in disp:
                    self.plotDt = disp["plotDt"]
            # Set up EPSP parameters.
            self.epspFreq = 100.0 # Used to generate single synaptic event
            self.epspWindow = 0.02 # Time of epspPlot to scan for pk/slope
            self.ex = 0.0005   # Electrode position for field recordings.
            self.ey = 0.0
            self.ez = 0.0
            self.fepspMin = -0.002 # 2 mm to the left of trode
            self.fepspMax = 0.001 # 1 mm to the right of trode
            epsp = ro.get( "epsp" )
            if epsp:
                if "epspFreq" in epsp:
                    self.epspFreq = epsp["epspFreq"]
                if "epspWindow" in epsp:
                    self.epspWindow = epsp["epspWindow"]
                if "electrodePosition" in epsp:
                    self.ex, self.ey, self.ez = epsp["electrodePosition"]
                if "epspDepthIntegMin" in epsp:
                    self.fepspMin = epsp["DepthIntegMin"]
                if "epspDepthIntegMax" in epsp:
                    self.fepspMax = epsp["DepthIntegMax"]
                        
        
    def configure( self, modelLookup ):
        """Sanity check on all fields. First, check that all the entities
        named in experiment have counterparts in the model definition"""
        for i in self.entities:
            #if not i.encode("ascii") in modelLookup:
            if not i in modelLookup:
                raise SimError( "Readout::configure: Error: object {} not defined in model lookup.".format( i ) )
        for i in self.ratioReferenceEntities:
            #if not i.encode("ascii") in modelLookup:
            if not i in modelLookup:
                raise SimError( "Readout::configure: Error: ratioReferenceEntity '{}' not defined in model lookup.".format( i ) )

    def digestSteadyStateRun( self, ref, ret ):
        if self.useNormalization:
            if self.normMode == "dose":
                # Here we have specified a distinct dose against which to
                # normalize. This is run as an extra data point, and has 
                #to be popped.
                assert( len( ret ) > 1 and len( ref ) == len( ret ) )
                referenceAtExtraDose = ref.pop()
                ref = [referenceAtExtraDose] * len( ref )
                tempret = ret.pop() # Pop the readout mol here too.
            elif self.normMode == "start": 
                ref = [ret[0]] * len( ret )
            elif self.normMode == "end": 
                ref = [ret[-1]] * len( ret )
            elif self.normMode == "min": 
                ref = [min(ret)] * len( ret )
            elif self.normMode == "max": 
                ref = [max(ret)] * len( ret )
            elif self.normMode == "presetTime": 
                print( "Probably you want sampling mode to be one of: start, end, min, max, dose. Defaulting to 'start'")
                ref = [ret[0]] * len( ret )
        else:
            ref = [self.quantityScale * 1.0] * len( ret )
        # The remaining case is that normMode == 'each', in which case we
        # compute the ref for each stimulus value. Ref goes through 
        # unchanged in this case.

        # Check for zeroes in the denominator
        eps = 1e-16
        if len( [ x for x in ref if abs(x) < eps ] ) > 0:
            raise SimError( "runDoser: Normalization failed due to zero denominator" )
        # Finally assign the simData.
        self.simData = [ x/y for x, y in zip( ret, ref ) ]

    def displayPlots( self, fname, modelLookup, stims, hideSubplots, exptType, bigFont = False ):
        if "doseresponse" in exptType:
            for i in stims[0].entities:
                #elms = modelLookup[i.encode("ascii")]
                #elms = modelLookup.get( i.encode("ascii") )
                elms = modelLookup.get( i )
                if not elms:
                    raise SimError( "displayPlots 1: could not find entity '{}'".format( i ) )
                for j in elms:
                    pp = PlotPanel( self, exptType, xlabel = str(j) +' ('+stims[0].quantityUnits+')', useBigFont = bigFont )
                    pp.plotme( fname, pp.ylabel, joinSimPoints = True )
        elif "barchart" in exptType:
            for i in self.entities:
                #elms = modelLookup[i.encode("ascii")]
                #elms = modelLookup.get( i.encode("ascii") )
                elms = modelLookup.get( i )
                if not elms:
                    raise SimError( "displayPlots 2: could not find entity '{}'".format(i) )
                for j in elms:
                    pp = PlotPanel( self, exptType, xlabel = str(j) +' ('+stims[0].quantityUnits+')', useBigFont = bigFont )
                    pp.plotbar( self, stims, fname )
        elif "timeseries" in exptType:
            tsUnits = self.quantityUnits
            '''
            if self.field in Readout.epspFields:
                tsUnits = 'mV'
            elif self.field in Readout.epscFields:
                tsUnits = 'pA'
            elif self.field in Readout.fepspFields:
                if not hideSubplots:
                    self.plotFepsps( fname, useBigFont = bigFont )
                    return
            elif self.useNormalization:
                tsUnits = 'Fold change'
            '''
            tsScale = convertQuantityUnits[tsUnits]
            if self.field in Readout.fepspFields:
                if not hideSubplots:
                    self.plotFepsps( fname, useBigFont = bigFont )
                    return

            ######################################
            pp = PlotPanel( self, exptType, useBigFont = bigFont )
            assert( len( self.plots ) > 0)
            numPts = len( self.plots[0] )
            assert( numPts > 0 )
            sumvec = np.zeros( numPts )
            scale = self.quantityScale
            if self.useNormalization:
                if self.normMode == "presetTime":
                    scale = tsScale * self.ratioReferenceValue
                elif len( self.ratioData ) > 0:
                    if self.normMode == "start" and self.ratioData[0] > 0.0:
                        scale = tsScale * self.ratioData[0]
                    elif self.normMode == "end" and self.ratioData[-1] > 0.0:
                        scale = tsScale * self.ratioData[-1]
                    elif self.normMode == "min" and min(self.ratioData) > 0.0:
                        scale = tsScale * min( self.ratioData )
                    elif self.normMode == "max" and max(self.ratioData) > 0.0:
                        scale = tsScale * max( self.ratioData )
                    elif self.normMode == "each" and max(self.ratioData) > 0.0:
                        scale = tsScale * max( self.ratioData )
                        # For 'each' we don't realy have a good way to do
                        # timeseries. So just use the biggest.

            '''
            if len( self.ratioData ) > 0:
                scale = tsScale * self.ratioData[0]
                print( "Scale 1: {} {} {}".format( scale, tsScale, self.ratioData ) )
            else:
                scale = tsScale * self.ratioReferenceValue
                print( "Scale 2: {} {} {}".format( scale, tsScale, self.ratioReferenceValue ) )
            print( "Scale 0: {} {} {}".format( scale, tsScale, self.normMode ) )
            '''

            for ypts in self.plots:
                tconv = convertTimeUnits[ self.timeUnits ]
                xpts = np.array( range( numPts)  ) * self.plotDt / tconv
                ypts /= scale
                sumvec += ypts
                if not hideSubplots:
                    # Plot summed components. Need to access name.
                    #plt.plot( xpts, ypts, 'r:', label = j.name )
                    plt.plot( xpts, ypts, 'r:' )
            plt.plot( xpts, sumvec, 'r--' )
            ylabel = pp.ylabel
            if self.field in ( Readout.epspFields + Readout.epscFields ):
                if self.field in Readout.epspFields:
                    plt.ylabel( '{} Vm ({})'.format( self.entities[0], tsUnits ) )
                else:
                    plt.ylabel( '{} holding current ({})'.format( self.entities[0], tsUnits ) )

                plt.figure(2)
                if self.useNormalization:
                    ylabel = '{} Fold change'.format( self.field )
            pp.plotme( fname, ylabel )

            ######################################

    def plotFepsps( self, fname, useBigFont = False ):
        #tconv = next( v for k, v in convertTimeUnits.items() if self.timeUnits in k )
        tconv = convertTimeUnits[ self.timeUnits ]
        assert( len( self.plots ) > 0 )
        numPts = len( self.plots[0] )
        xpts = np.array( range( numPts)  ) * self.plotDt / tconv
        sumvec = np.zeros( numPts )
        for i, wt in zip( self.plots, self.wts ):
            # I'm going to plot the original currents rather than the
            # variously scaled contributions leading up to the fEPSP
            ypts = i * 1e12   # Hack, hard code currents in pA
            plt.plot( xpts, ypts, 'r:' )
            sumvec += ypts
        plt.plot( xpts, sumvec, 'r--' )
        plt.xlabel( "time ({})".format( self.timeUnits) )
        plt.ylabel( "Compartment currents Im (pA)" )
        plt.figure(2)
        pp = PlotPanel( self, "timeseries", useBigFont = useBigFont )
        pp.plotme( fname, "fEPSP (mV)" )

    def doScore( self, scoringFormula ):
        #assert( len(self.data) == len( self.simData ) )
        score = 0.0
        numScore = 0.0
        dat = []
        if self.data:
            dvals = [i[1] for i in self.data]
            dat = self.data
        elif self.bardata:
            dvals = [i["value"] for i in self.bardata]
            dat = [ [0, i["value"], i["stderr"] ] for i in self.bardata ]
        datarange = max( dvals ) - min( dvals )
        if self.tabulateOutput:
            print( "{:>12s}   {:>12s}  {:>12s}  {:>12s}".format( "t", "expt", "sim", "sem" ) )
        for i, sim in zip( dat, self.simData ):
            #sim /= self.quantityScale
            t = i[0]
            expt = i[1]
            sem = i[2]
            if self.tabulateOutput:
                print( "{:12.3f}   {:12.3f}  {:12.5g}  {:12.3f}".format( t, expt, sim, sem ) )
            #print "Formula = ", scoringFormula, eval( scoringFormula )
            score += eval( scoringFormula )
            numScore += 1.0

        if numScore == 0:
            return -1
        return score/numScore

    def directParamScore( readouts, scoringFormula ):
        score = 0.0
        numScore = 0.0
        for d in readouts.directParamData:
            entity = d["entity"]
            qs = convertQuantityUnits[ d["units"] ]
            expt = d["value"] * qs
            sem = d["stderr"] * qs
            sim = sw.getObjParam( entity, str( d["field"] ) )
            datarange = max( expt, sim, 1e-9 )
            score += eval( scoringFormula )
            numScore += 1.0

        '''
        for rd in readouts:
            dvals = [i[1]*rd.quantityScale for i in rd.data]
            for d in rd.data:
                entity = d[0]
                expt = d[1]*rd.quantityScale
                sem = d[2]*rd.quantityScale
                sim = sw.getObjParam( entity, rd.field )
                datarange = max( expt, sim, 1e-9 )
                score += eval( scoringFormula )
                numScore += 1.0
        '''
        #print( "direct score of {}".format( score / numScore ) )
        if numScore == 0:
            return -1
        return score/numScore
    directParamScore = staticmethod( directParamScore )

##########################################################################

class Model:
    """The Model class specifies the baseline model against which the 
    experiment protocol has been developed. It is expected that the
    protocol should run and generate a valid score against this baseline
    model. Typically actual models will be derived from this original 
    one.
    The key additional field here is the 'subset'. This defines the 
    subset of the entire model that should be used for running the protocol.
    This subset may be defined as a 'group', which is is like a directory
    and is a standarad model organizational structure in MOOSE. It may,
    less cleanly, be defined as a list of relevant molecules and reactions.
    In keeping with the SED-ML convention, changes to the model are also
    handled by the Model class. Two kinds of changes are supported: \n
    - parameter changes, in which fields get set. \n
    - structural changes, in which the model itself is altered. \n
    """
    def __init__( self, findsim, mapFile ):
        self.modelSubset = []
        self.parameterChange = []
        self.itemsToDelete = []
        mod = findsim.get( "Modifications" )
        if mod:
            if "subset" in mod:
                self.modelSubset = mod[ "subset" ]
            if "itemsToDelete" in mod:
                self.itemsToDelete = mod[ "itemsToDelete" ]
            if "parameterChange" in mod:
                self.parameterChange = mod[ "parameterChange" ]


        if mapFile == "":
            mapFile = findsim["Metadata"].get( "testMap" )
            if not mapFile:
                raise SimError( "Map file not specified" )
        if mapFile.split('.')[-1] != 'json':
            raise SimError( "Map file '{}' not in JSON format".format( mapFile ) )

        self._tempModelLookup = {}
        try: 
            with open( mapFile ) as json_file:
                m1 = json.load( json_file )
                m2 = {}
                for key, val in m1.items():
                    #m2[ key.encode( "ascii" ) ] = [ i.encode( "ascii" ) for i in val ]
                    m2[ str(key) ] = [ str(i) for i in val ]
            self._tempModelLookup = m2
        except:
            raise SimError( "Map file name {} not found".format(mapFile) )
        #print( "LOADED MAPFILE {}".format( mapFile ) )

    def modify( self, erSPlist, modelWarning):
        '''
        Semantics: There are two specifiers: what to save (modelSubset) 
        and what to delete (itemstodelete). 
        modelSubset: A list of object identifier strings.
        - If the object is a group or compartment: 
                - it is saved
                - everything under it is saved
                - Parent group and compartment is saved, recursively
                - Siblings are NOT saved.
         - If the object is a pool, reaction, etc:
                - it is saved
                - Parent group and compartment is saved, recursively
                - Siblings are NOT saved.
        itemstodelete: A list of object identifier strings.
        - If the object is a group or compartment: 
            - It is deleted
            - Everthing under it is deleted
        - If the object is a regular pool, reaction etc:
            - It is deleted
            - Everthing under it is deleted. Note that a pool might have
                multiple enzyme sites. All of them will be deleted.
        After all this is done, there is a cleanup:
            - If a reaction or enzyme has had a substrate or product
                deleted, it is deleted. Otherwise we would end up with
                dangling reactions.
        '''
        sw.deleteItems( [ ( i, "delete") for i in self.itemsToDelete] )
        if len( self.modelSubset ) > 0 and not "all" in self.modelSubset:
            sw.subsetItems( self.modelSubset )
        #Function call for checking dangling Reaction/Enzyme/Function's
        sw.pruneDanglingObj( erSPlist)
        #print( "{}".format( self.parameterChange ) )
        sw.changeParams( [ [i["entity"], i["field"], i["value"] * convertQuantityUnits[ i["units"] ] ] for i in self.parameterChange] )

            
##########################################################################
# Utility functions needed by Model class.

class PauseHsolve:
    def __init__(self, optimizeElec = False):
        self.optimizeElec = optimizeElec
        self.epspSettle = 0.5
        self.stimSettle = 2.0

    def setHsolveState(self, state):
        if not self.optimizeElec:
            return
        sw.setHsolveState( state, self )

#######################################################################
class Qentry():
    def __init__( self, t, entry, val ):
        self.t = t
        self.entry = entry
        self.val = val

    def __lt__( self, other ):
        return self.t < other.t

def putStimsInQ( q, stims, pauseHsolve ):
    for i in stims:
        for j in i.data:
            if len(j) == 0:
                continue
            elif len(j) == 1:
                val = 0.0
            else:
                val = float(j[1]) * i.quantityScale
            t = float(j[0])*i.timeScale
            heapq.heappush( q, Qentry( t, i, val ) )
            # Below we tell the Hsolver to turn off or on for elec calcn.
            if i.field in ['Im', 'current', 'Vclamp'] or (i.field=='rate' and 'syn' in i.entities[0]) :
                if val == 0.0:
                    heapq.heappush( q, Qentry(t+pauseHsolve.stimSettle, pauseHsolve, 0) )
                else:
                    heapq.heappush( q, Qentry(t, pauseHsolve, 1) ) # Turn on hsolve


def putReadoutsInQ( q, readouts, pauseHsolve ):
    stdError  = []
    plotLookup = {}
    if readouts.field in Readout.postSynFields:
        for j in range( len( readouts.data ) ):
            t = float( readouts.data[j][0] ) * readouts.timeScale
            heapq.heappush( q, Qentry(t, pauseHsolve, 1) ) # Turn on hsolve
            heapq.heappush( q, Qentry(t, readouts.stim, readouts.epspFreq) )
            heapq.heappush( q, Qentry(t+1.0/readouts.epspFreq, readouts.stim, 0) )
            heapq.heappush( q, Qentry(t+readouts.epspWindow, readouts, j) )# Measure after EPSP
            heapq.heappush( q, Qentry(t+readouts.epspWindow+pauseHsolve.epspSettle, pauseHsolve, 0) )

    else:
        # We push in the index of the data entry so the readout can
        # process it when it is run. It will grab both the readout and
        # ratio reference if needed.
        for j in range( len( readouts.data ) ):
            t = float( readouts.data[j][0] ) * readouts.timeScale
            heapq.heappush( q, Qentry(t, readouts, j) )

    if readouts.useNormalization and readouts.normMode == "presetTime":
        # We push in -1 to signify that this is to get ratio reference
        heapq.heappush( q, Qentry(float(readouts.ratioReferenceTime)*readouts.timeScale, readouts, -1) )

def doReadout( qe, model ):
    ''' 
    This function obtains readout values from the simulation. 
    In all cases it checks to see if it should load in a simulation 
    readout. In addition, there are two options for the ratio reference:\n
    1. if ratioReferenceTime is < zero,
        -then at every readout time point the ratio reference shd be noted,
        and this should be applied to readout molecule values while 
        calculating the ratio sim/ratioRefMol \n
    2. if ratioReferenceTime is >=0.0, then the entire ratio reference 
        array is to be filled with the value of reference entity at 
        t=ratioReferenceTime.
    '''
    readout = qe.entry
    val = int(round( ( qe.val ) ) )
    if readout.field in (Readout.epspFields + Readout.epscFields):
        readout.plots, readout.plotDt = sw.fillPlots()
        doEpspReadout( readout )
    elif readout.field in Readout.fepspFields:
        readout.plots, readout.plotDt = sw.fillPlots()
        doFepspReadout( readout )
    elif val == -1: # This is a special event to get RatioReferenceValue
        readout.ratioReferenceValue = sw.sumFields( readout.ratioReferenceEntities, readout.field )
    else:
        doEntityAndRatioReadout(readout, readout.field)

def doFepspReadout( readout ):
    n = int( round( readout.epspWindow / readout.plotDt ) )
    #n = int( round( readout.epspWindow / readout.epspPlot.dt ) )
    assert( n > 5 )
    assert( len( readout.plots ) == len( readout.wts ) )
    pts = np.zeros( n )
    for i, wt in zip( readout.plots, readout.wts ):
        pts += i[-n:] * wt
    pts /= len( readout.wts )
    #print( "DOING EPSP READOUT WITH " +  readout.field )
    #print( ["{:.3g} ".format( x ) for x in pts] )
    if "slope" in readout.field:
        dpts = pts[1:] - pts[:-1]
        slope = max( abs( dpts ) )/readout.plotDt
        v = slope / readout.quantityScale
    elif "peak" in readout.field:
        pts -= pts[0]
        pk = max( abs(pts) )
        v = pk / readout.quantityScale
    readout.simData.append( v )
    readout.ratioData.append( v )

def doEpspReadout( readout ):
    n = int( round( readout.epspWindow / readout.plotDt ) )
    assert( n > 5 )
    assert( len( readout.plots ) > 0 )
    assert( len( readout.plots[0] ) > 5 )
    pts = readout.plots[0][-n:]
    ratioReference = 1.0
    if "slope" in readout.field:
        dpts = pts[1:] - pts[:-1]
        slope = max( abs( dpts ) )/readout.plotDt
        v = slope / readout.quantityScale
    elif "peak" in readout.field:
        pts -= pts[0]
        pk = max( abs(pts) )
        v = pk / readout.quantityScale
    readout.simData.append( v )
    readout.ratioData.append( v )

def doEntityAndRatioReadout( readout, field ):
    sim = sw.sumFields( readout.entities, field )
    readout.simData.append( sim/readout.quantityScale )
    ratioReference = 1.0
    if readout.useNormalization:
        ratioReference = sw.sumFields( readout.ratioReferenceEntities, field )
    readout.ratioData.append( ratioReference )

def processReadouts( readouts, scoringFormula ):
    numScore  = 0
    score = 0.0
    score += readouts.doScore( scoringFormula )
    numScore += 1
    return score/numScore


##########################################################################
def parseAndRun( model, stims, readouts ):
    q = []
    putStimsInQ( q, stims, model.pauseHsolve )
    putReadoutsInQ( q, readouts, model.pauseHsolve )

    sw.reinitSimulation()
    #model.pauseHsolve.setHsolveState( 0 )
    for i in range( len( q ) ):
        qe = heapq.heappop( q )
        currt = sw.getCurrentTime()
        if ( qe.t > currt ):
            sw.advanceSimulation( qe.t - currt )
        if isinstance( qe.entry, Stimulus ):
            sw.deliverStim( qe )
            #print( "DELIVER STIM {} {} {} {}".format( qe.entry.entities, qe.entry.field, qe.entry.data, qe.val ) )
        elif isinstance( qe.entry, Readout ):
            doReadout( qe, model )
        elif isinstance( qe.entry, PauseHsolve ):
            qe.entry.setHsolveState( int(qe.val) )

    # Normalize. Applies to cases where we do a special run for a 
    # single normalization value that scales all points. Since it
    # defaults to 1, we can simply apply always.
    norm = 1.0
    if readouts.useNormalization:
        if readouts.normMode == "start":
            norm = readouts.ratioData[0]
        elif readouts.normMode == "end":
            norm = readouts.ratioData[-1]
        elif readouts.normMode == "min":
            norm = min( readouts.ratioData )
        elif readouts.normMode == "max":
            norm = max( readouts.ratioData )
        elif readouts.normMode == "presetTime":
            # The event Q has caused this special value to be recorded.
            norm = readouts.ratioReferenceValue
        elif readouts.normMode == "dose":
            print( "Warning: trying to normalize time-series to a dose. Probably you want to use start or a preset time. Using start." )
            norm = readouts.ratioData[0]

    eps = 1e-16
    if readouts.useNormalization and readouts.normMode == "each":
        if len( [ y for y in readouts.ratioData if abs(y) < eps ] ) > 0:
            raise SimError( "runDoser: Normalization failed due to zero denominator" )
        readouts.simData = [ x/y for x, y in zip(readouts.simData, readouts.ratioData) ]
    else:
        if abs(norm) < eps:
            raise SimError( "runDoser: Normalization failed due to zero denominator" )
        readouts.simData = [ x/norm for x in readouts.simData ]
    # Collect detailed time series
    readouts.plots, readouts.plotDt = sw.fillPlots()
    score = processReadouts( readouts, model.scoringFormula )

    return score


##########################################################################
def parseAndRunDoser( model, stims, readouts ):
    if len( stims ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs \
            exactly one stimulus block, {} defined".format( len(stims)) )
    numLevels = len( readouts.data )
    
    if numLevels == 0:
        raise SimError( "parseAndRunDoser: no dose (stimulus) levels defined for run" )
    
    runTime = readouts.settleTime
    
    if runTime <= 0.0:
        print( "Currently unable to handle automatic settling to steady-state in doseResponse, using default 1000 s." )
        runTime = 1000
    
    doseMol = ""
    #Stimulus Molecules
    #Assuming one stimulus block, one molecule allowed
    runDoser( model, stims[0], readouts )
    score = processReadouts( readouts, model.scoringFormula )
    return score

def runDoser( model, stim, readout ):
    stimList = []
    responseList = []
    EPS = 1e-9
    for dose, response, sem in readout.data:
        stimList.append( [ (stim.entities[0], stim.field, dose, stim.quantityScale), ] )
    if len( readout.ratioReferenceEntities ) > 0 and readout.ratioReferenceTime > EPS:
        # Add another entry for the global reference readout.
        stimList.append( [ (stim.entities[0], stim.field, readout.ratioReferenceDose, stim.quantityScale), ] )
        #print( ">>>>>>>>> {} {} {} {}".format( stim.entities[0], stim.field, readout.ratioReferenceDose, stim.quantityScale ) )
    responseList = [ readout.entities, readout.field, readout.ratioReferenceEntities, readout.field ]
    ret, ref = sw.steadyStateStims( stimList, responseList, isSeries = True, settleTime = readout.settleTime )
    if len( readout.ratioReferenceEntities ) > 0 and readout.ratioReferenceTime < EPS:
        # Special case where the extra entry is the value at reset time.
        refLast = sw.getObjParam(readout.ratioReferenceEntities[0], "concInit" )
        ret.append( ret[-1] )
        ref.append( refLast )

    readout.digestSteadyStateRun( ref, ret )
    # and here we go about extracting the values from ret and ref.

##########################################################################

def runBarChart( model, stims, readout ):
    ''' The possible stimuli in the bar chart are each defined in a
    separate stim.
    The Readouts bardata is an array with each entry a dict:
    {"stimulus": ["stim1","stim2"...], "value": val, "stderr": ser}
    Stim1, stim2 are the names/labels for the stims to be applied
    '''

    stimSource = []
    stimList = []

    stimSource = {}
    for s in stims:
        #print ("SSSSSSSSSSSSS= {}".format( s.data ) )
        stimEntry = ( s.entities[0], s.field, s.data[0][1], s.quantityScale )
        stimSource[ s.label ] = stimEntry
    for i in readout.bardata:
        stimLine = [ stimSource[ j ] for j in i["stimulus"] ]
        stimList.append( stimLine )

    responseList = [ readout.entities, readout.field, readout.ratioReferenceEntities, readout.field ]
    # Some fuzzy normalization stuff
    if readout.useNormalization and readout.normMode == "presetTime":
        stimList.append( [] )
    # And here we go:
    ret, ref = sw.steadyStateStims( stimList, responseList, isSeries = False, settleTime = readout.settleTime )
    # Extract values.
    readout.digestSteadyStateRun( ref, ret )

def parseAndRunBarChart( model, stims, readouts ):
    numLevels = len( readouts.bardata )
    
    if numLevels == 0:
        raise SimError( "parseAndRunBarChart: no stimulus levels defined for run" )
    
    runTime = readouts.settleTime
    
    if runTime <= 0.0:
        print( "Currently unable to handle automatic settling to steady-state in Bar Charts, using default 300 s." )
        runTime = 300

    runBarChart( model, stims, readouts )

    score = processReadouts( readouts, model.scoringFormula )
    return score

##########################################################################

class PlotPanel:
    def __init__( self, readout, exptType, xlabel = '', useBigFont=False ):
        self.name=[]
        for i in readout.entities:
            self.name.append( i )
        self.exptType = exptType
        self.useXlog = readout.useXlog
        self.useYlog = readout.useYlog
        if len( xlabel ) > 0:
            self.xlabel = xlabel
        else:
            self.xlabel = 'Time ({})'.format( readout.timeUnits )
        self.labelFontSize = 'xx-large' if useBigFont else 'large'
        self.tickFontSize = 'x-large' if useBigFont else 'medium'

        if readout.data:
            self.xpts = [ i[0] for i in readout.data]
            self.expt = [ i[1] for i in readout.data]
            self.yerror = [ i[2] for i in readout.data]
        elif readout.bardata:
            self.xpts = [ i["value"] for i in readout.bardata]
            self.expt = [ i["value"] for i in readout.bardata]
            self.yerror = [ i["stderr"] for i in readout.bardata]
        self.sim = readout.simData # Ratios already handled at this stage
        #print( "xplts = {}, sim = {}, expt = {}, yerror = {}".format( len( self.xpts), len( self.sim ), len( self.expt), len( self.yerror )) )
        self.sumName=""
        for i in self.name:
            self.sumName += i
            self.sumName += " "
            self.ylabel = '{} {} ({})'.format(i, readout.field, readout.quantityUnits ) #problem here.check so that y-axis are for diff plts not in one plot

    def convertBarChartLabels( self, readout, stims ):
        ret = []
        #doseMol = [ i[0] for i in stim.data ]
        doseMol = [ i.label for i in stims ]
        for i in readout.bardata:
            ticklabel = ""
            for j in doseMol:
                if j in i["stimulus"]:
                    ticklabel += j + '\n'
                else:
                    ticklabel += '-\n'

            '''
            for j in range( len( i[0] ) ):
                if i[0][j] == '1' or i[0][j] == '+':
                    ticklabel += doseMol[j] + '\n'
                else:
                    ticklabel += '-\n'
            '''
            ret.append( ticklabel )
        return ret


    def plotbar( self, readout, stims, scriptName ):
        barpos = np.arange( len( self.sim ) )
        width = 0.35 # A reasonable looking bar width
        exptBar = plt.bar(barpos - width/2, self.expt, width, yerr=self.yerror, color='SkyBlue', label='Experiment')
        simBar = plt.bar(barpos + width/2, self.sim, width, color='IndianRed', label='Simulation')
        plt.xlabel( "Stimulus combinations", fontsize=self.labelFontSize)
        plt.ylabel( self.ylabel, fontsize = self.labelFontSize )
        plt.title( scriptName, fontsize = self.labelFontSize )
        plt.legend( loc="upper left", fontsize = self.tickFontSize )
        #ticklabels = [ i["stimulus"] for i in readout.bardata ] 
        #assert len( ticklabels ) == len( barpos )
        ticklabels = self.convertBarChartLabels( readout, stims )
        plt.xticks( barpos, ticklabels, fontsize = self.tickFontSize  )
        plt.tick_params( labelsize=self.tickFontSize )

    def plotme( self, scriptName, ylabel, joinSimPoints = False ):
        sp = 'ro-' if joinSimPoints else 'ro'
        nx = len( self.xpts )
        ss = self.sim[:nx]
        if self.useXlog:
            if self.useYlog:
                plt.loglog( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                plt.loglog( self.xpts, ss, sp, label = 'sim', linewidth='2' )
            else:
                plt.semilogx( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                plt.semilogx( self.xpts, ss, sp, label = 'sim', linewidth='2' )
        else:
            if self.useYlog:
                plt.semilogy( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                plt.semilogy( self.xpts, ss, sp, label = 'sim', linewidth='2' )
            else:
                plt.plot( self.xpts, self.expt,'bo-', label = 'experiment', linewidth='2' )
                plt.errorbar( self.xpts, self.expt, yerr=self.yerror )
                plt.plot( self.xpts, ss, sp, label = 'sim', linewidth='2' )

        plt.xlabel( self.xlabel, fontsize = self.labelFontSize )
        plt.ylabel( ylabel, fontsize = self.labelFontSize )
        plt.title( scriptName, fontsize = self.labelFontSize)
        plt.legend( fontsize=self.tickFontSize, loc="upper right")
        plt.tick_params( labelsize=self.tickFontSize )

########################################################################

def saveTweakedModel( origFname, dumpFname, mapFile, scaleParam ):
    # scaleParam is [(entity, field, scale), ...]
    # Design this function to be completely independent of any tsvs, which
    # may introduce their own changes into the reference model. So it
    # does a fresh load, tweaks the params, and saves.
    fname, extn = os.path.splitext( dumpFname )
    if extn == '.g' or extn == '.xml':
        localSW = simWrapMoose.SimWrapMoose( mapFile = mapFile, ignoreMissingObj = True, silent = True )
    elif extn == '.json':
        localSW = simWrapHillTau.SimWrapHillTau( mapFile = mapFile, ignoreMissingObj = True, silent = True )
    else:
        print( "Warning: dumpTweakedModel: File format '{}' not known".format( extn ) )
        return
    sp = []
    for i in scaleParam:
        sp.extend( i )
    localSW.deleteSimulation()
    localSW.loadModelFile( origFname, dummyModify, sp, dumpFname, "" )

def dummyModify( erSPlist, modelWarning ):
    #raise SimError( "dummyModify: should never be called\n")
    print( ".", end = "" )

def loadJson( fname, mapFile ):
    stims = []
    readouts = []
    with open( fname ) as fd:
        findsim = json.load( fd )
    relpath = os.path.dirname( __file__ )
    if relpath != '': # outside local directory
        #relpath = relpath + '/'
        fs = relpath + '/' + fschema
    else:
        fs = fschema

    with open( fs ) as _schema:
        schema = json.load( _schema )
    jsonschema.validate( findsim, schema )
    expt = Experiment( findsim["Metadata"], findsim["Experiment"] )
    stims = Stimulus.load( findsim ) # Stimuli are an optional argument
    readouts = Readout( findsim["Readouts"] )
    model = Model( findsim, mapFile ) # mods are an optional argument.
    return expt, stims, readouts, model

def runit( expt, model, stims, readouts ):
    for i in stims:
        i.configure( model._tempModelLookup )
    readouts.configure( model._tempModelLookup )

    if "doseresponse" in expt.exptType:
        return parseAndRunDoser( model, stims, readouts )
    elif "timeseries" in expt.exptType:
        return parseAndRun( model, stims, readouts )
    elif "barchart" in expt.exptType:
        return parseAndRunBarChart( model, stims, readouts )
    else:
        return 0.0

def main():
    """ This program handles loading a kinetic model, and running it
 with the specified stimuli. The output is then compared with expected output to generate a model score.
    """
    parser = argparse.ArgumentParser( description = 'FindSim argument parser\n'
    'This program loads a kinetic model, and runs it with the \n'
    'specified stimuli. The output is then compared with expected output \n'
    'specified in the same file, to generate a model score.\n'
    )

    parser.add_argument( 'script', type = str, help='Required: filename of experiment spec, in json format.')
    parser.add_argument( '-map', '--map', type = str, help='Optional: mapping file from tsv names to sim-specific strings. JSON format.', default = "" )
    #parser.add_argument( '-schema', '--schema', type = str, help='Optional: Schema for json version of the findSim experiment definition. JSON format.', default = "findSimSchema.json" )
    parser.add_argument( '-d', '--dump_subset', type = str, help='Optional: dump selected subset of model into named file', default = "" )
    parser.add_argument( '-m', '--model', type = str, help='Optional: model filename, .g or .xml', default = "" )
    parser.add_argument( '-p', '--param_file', type = str, help='Optional: Generate file of tweakable params belonging to selected subset of model', default = "" )
    parser.add_argument( '-score', '--score_func', type = str, help='Optional: specify scoring function for comparing expt and sim.', default = defaultScoreFunc )
    parser.add_argument( '-t', '--tabulate_output', action="store_true", help='Flag: Print table of plot values. Default is NOT to print table' )
    parser.add_argument( '-hp', '--hide_plot', action="store_true", help='Hide plot output of simulation along with expected values. Default is to show plot.' )
    parser.add_argument( '-hs', '--hide_subplots', action="store_true", help='Hide subplot output of simulation. By default the graphs include dotted lines to indicate individual quantities (e.g., states of a molecule) that are being summed to give a total response. This flag turns off just those dotted lines, while leaving the main plot intact.' )
    parser.add_argument( '-bf', '--big_font', action="store_true", help='Use larger font size in plots, useful for generating figures for presentation. Default is small font.' )
    parser.add_argument( '-o', '--optimize_elec', action="store_true", help='Optimize electrical computation. By default the electrical computation runs for the entire duration of the simulation. With this flag the system turns off the electrical engine except during the times when electrical stimuli are being given. This can be *much* faster.' )
    parser.add_argument( '-s', '--scale_param', nargs=3, default=[],  help='Scale specified object.field by ratio.' )
    parser.add_argument( '-settle_time', '--settle_time', type=float, default=0,  help='Run model for specified settle time and return dict of {path,conc}.' )
    parser.add_argument( '-imo', '--ignore_missing_obj', action="store_true", help='Flag, default False. When set the code ignores references to missing objects. Normally it would throw an error.' )
    parser.add_argument( '-v', '--verbose', action="store_true", help='Flag, default False. When set, prints out diagnostics such as references not found, or automatically deleted entities after various checks for dangling reactions.' )
    args = parser.parse_args()
    simWrap = ""
    if args.model.split( '.' )[-1] == "json":
        simWrap = "HillTau"
    innerMain( args.script, scoreFunc = args.score_func, modelFile = args.model, mapFile = args.map, dumpFname = args.dump_subset, paramFname = args.param_file, hidePlot = args.hide_plot, hideSubplots = args.hide_subplots, bigFont = args.big_font, optimizeElec = args.optimize_elec, silent = not args.verbose, scaleParam = args.scale_param, settleTime = args.settle_time, tabulateOutput = args.tabulate_output, ignoreMissingObj = args.ignore_missing_obj, simWrap = simWrap )

def innerMain( exptFile, scoreFunc = defaultScoreFunc, modelFile = "", mapFile = "", dumpFname = "", paramFname = "", hidePlot = False, hideSubplots = True, bigFont = False, optimizeElec=True, silent = False, scaleParam=[], settleTime = 0, settleDict = {}, tabulateOutput = False, ignoreMissingObj = False, simWrap = "" ):
    ''' If *settleTime* > 0, then we need to return a dict of concs of
    all variable pools in the chem model obtained after loading in model, 
    applying all modifications, and running for specified settle time.\n
    If the *settleDict* is not empty, then the system goes through and 
    matches up pools to assign initial concentrations.
    '''

    global pause
    global sw
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    modelWarning = ""
    expt, stims, readouts, model = loadJson( exptFile, mapFile )
    model.scoringFormula = scoreFunc # Override the earlier version.
    readouts.tabulateOutput = tabulateOutput

    if mapFile == "" and modelFile == "":
        model.fileName = expt.testModel
        mapFile = expt.testMap
    if modelFile != "":
        model.fileName = modelFile
    else:
        model.fileName = expt.testModel
    if model.fileName.split('.')[-1] == "json":
        simWrap = "HillTau"
    if simWrap == "":
        sw = simWrapMoose.SimWrapMoose( mapFile = mapFile, ignoreMissingObj = ignoreMissingObj, silent = silent )
    elif simWrap == "HillTau":
        sw = simWrapHillTau.SimWrapHillTau( mapFile = mapFile, ignoreMissingObj = ignoreMissingObj, silent = silent )
    else:
        sw = simWrap.SimWrap( ignoreMissingObj = ignoreMissingObj )
    model.pauseHsolve = PauseHsolve( optimizeElec )
    # First we load in the model using EE so it is easier to tweak
    try:
        if not os.path.isfile(model.fileName):
            raise SimError( "Model file name {} not found".format( model.fileName ) )
        fileName, file_extension = os.path.splitext(model.fileName)
        sw.loadModelFile( model.fileName, model.modify, scaleParam, dumpFname, paramFname )

        if expt.exptType == 'directparameter':
            t0 = time.time()
            score = Readout.directParamScore( readouts, model.scoringFormula )
            elapsedTime = time.time() - t0

            if not hidePlot:
                print( "Score = {:.3f} for\t{}\tElapsed Time = {:.1f} s".format( score, os.path.basename(exptFile), elapsedTime ) )
                #plt.figure(1)
                #readouts.displayPlots( exptFile, model._tempModelLookup, stims, hideSubplots, expt.exptType, bigFont = bigFont )
                #plt.show()
            #print( "Score = {:.3f} for\t{}\tElapsed Time = {:.1f} s".format( score, os.path.basename(exptFile), elapsedTime ) )
            sw.deleteSimulation()
            return score, elapsedTime

        hasVclamp = False
        if len( stims ) > 0:
            readoutStim = stims[0]
        else:
            redoutStim = ""
        for i in stims:
            if i.field.lower() == 'vclamp':
                hasVclamp = True
                vpath = sw.buildVclamp( i )
                model._tempModelLookup['vclamp'] = [vpath,]
            elif i.field.lower() == 'inject':
                readoutStim = i
            if len(i.entities) > 0 and i.entities[0].lower() == 'syninput':
                readoutStim = i
            if expt.exptType in ['barchart', 'doseresponse']:
                sw.changeParams( [( i.entities[0], "isBuffered", 1 ),] )
        if readouts.field in Readout.postSynFields:
            readouts.stim = readoutStim 
        sw.makeReadoutPlots( [ readouts ] )

        sw.buildSolver( "gsl", useVclamp = hasVclamp )
        ##############################################################
        # Here we handle presettling. First to generate, then to apply
        # the dict of settled values.
        if settleTime > 0:
            return sw.presettle( settleTime ), 0.0

        sw.assignPresettle( settleDict )
        ##############################################################

        t0 = time.time()
        score = runit( expt, model,stims, readouts  )
        elapsedTime = time.time() - t0
        if not hidePlot:
            plt.figure(1)
            readouts.displayPlots( exptFile, model._tempModelLookup, stims, hideSubplots, expt.exptType, bigFont = bigFont )
            plt.show()
            print( "Score = {:.4f} for\t{}\tElapsed Time = {:.1f} s".format( score, os.path.basename(exptFile), elapsedTime ) )
        sw.deleteSimulation()
        return score, elapsedTime
        
    except SimError as msg:
        if not silent:
            print( "Error: findSim failed for exptDefn {}: {}".format(exptFile, msg ))
        sw.deleteSimulation()
        if __name__ == '__main__':
            traceback.print_exc()
        return -1.0, 0.0
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()

