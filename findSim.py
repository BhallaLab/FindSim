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
**           copyright (C) 2003-2018 Upinder S. Bhalla. and NCBS
**********************************************************************/

'''
from __future__ import print_function
import heapq
import pylab
import numpy as np
import sys
import traceback
import argparse
import os
import re
import time
import imp      # This is apparently deprecated in Python 3.4 and up
from simError import SimError
import simWrap
import simWrapMoose


convertTimeUnits = {('sec','s') : 1.0, 
    ('ms','millisec', 'msec') : 1e-3,('us','microsec') : 1e-6, 
    ('ns','nanosec') : 1e-9, ('min','m') : 60.0, 
    ('hours','hrs') : 3600.0, "days": 86400.0}
#convertConcUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 'nM':1.0e-6, 'pM': 1.0e-9, 'number':1.0, 'ratio':1.0 }
#convertVoltageUnits = { 'V': 1, 'mV': 0.001, 'uV': 1.0e-6, 'nV':1.0e-9 }
#convertCurrentUnits = { 'A': 1, 'mA': 0.001, 'uA': 1.0e-6, 'nA':1.0e-9, 'pA':1.0e-12 }
convertQuantityUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 
        'nM':1.0e-6, 'pM': 1.0e-9, 'number':1.0, 'ratio':1.0, 
        'V': 1.0, 'mV': 0.001, 'uV': 1.0e-6, 'nV':1.0e-9,
        'A': 1.0, 'mA': 0.001, 'uA': 1.0e-6, 'nA':1.0e-9, 'pA':1.0e-12,
        'Hz': 1.0, '1/sec':1.0, 'sec':1.0, 's':1.0, 'min':60.0, 
        'mV/ms':1.0, '%':100.0, 'Fold change':1.0 }

# Shifted to Readout class as static fields.
#epspFields = [ 'EPSP_peak', 'EPSP_slope', 'IPSP_peak', 'IPSP_slope' ]
#epscFields = [ 'EPSC_peak', 'EPSC_slope', 'IPSC_peak', 'IPSC_slope' ]
#fepspFields = [ 'fEPSP_peak', 'fEPSP_slope', 'fIPSP_peak', 'fIPSP_slope' ]
#elecFields = ['Vm', 'Im', 'current'] + epspFields + epscFields

sw = ""         #default dummy value for SimWrap

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
    def __init__( self, 
            exptType = 'timeSeries',
            exptSource = 'paper', # Options are paper, inHouse, database
            citationId = '',  # Journal name/ in-house project name/ database
            authors = '',   # Who did the work
            journal = '',     # journal
            temperature = 22    # Degrees Celsius
        ):
        self.exptSource = exptSource

        """This defines what kind of data is in the experiment. 
        timeSeries is the most elementary experiment: Monitor a model
        value at a succesion of points in time. Other options are
        doseResponse, barchart, and more.
        """
        self.exptType = exptType.lower()
        self.citationId = citationId
        self.authors = authors
        self.journal = journal
        self.temperature = temperature

    def load( fd ):
        doneContext = False
        arg = {}
        for line in fd:
            cols = line.split('\t')
            c0 = cols[0].strip()
            if doneContext and (len( cols ) == 0 or c0 == '' or c0.isspace()):
                break
            if c0 == "Experiment context":
                doneContext = True
                continue
            for i in Experiment.argNames:
                if keywordMatches( c0, i ):
                    arg[i] = str.strip( nonBlank( cols ) )
                    continue
        return Experiment( **arg )

    load = staticmethod( load )

Experiment.argNames = ['exptType', 'exptSource', 'citationId', 'authors', 'journal', 'temperature' ]

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
    def __init__( self,
            timeUnits = 's',
            quantityType = 'chem', # Could be chem, elec, mech, or spikes
            quantityUnits = 'mM',
            quantityScale = 1.0,    # Go from quantity units to SI.
            entities = '',
            field = '',
            data = []
        ):
        if timeUnits != " ":
            self.timeUnits = timeUnits
        """timeUnits may be us, ms, s, min, hours, days"""
        #self.timeScale = convertTimeUnits[ timeUnits ]
        self.timeScale = next(v for k, v in convertTimeUnits.items() if timeUnits in k)
        """timeScale is timeUnits scaled to seconds"""
        self.quantityUnits = quantityUnits.strip()
        if self.quantityUnits in convertQuantityUnits:
            self.quantityScale = convertQuantityUnits[ self.quantityUnits ]
        else:
            raise SimError(" Stimulus::__init__: quantity units not known: " + self.quantityUnits )
        temp = entities.split( ',' )
        self.entities = [ i for i in temp if len(i) > 0 ]
        """Name of the model entity to modify for the stimulus. 
        Typically a molecule name, or a compartment in a neuron."""
        self.field = field
        """Name of the field associated with the entity. For example,
        conc for a molecule, or currentInjection for compartment"""
        self.data = data
        """List of pairs of numbers for stimulus, Each row is [time or dose, quantity]"""


        
    def load( fd ):
        arg, data, param, struct, modelLookup = innerLoad( fd, Stimulus.argNames, dataWidth = 2 )
        stim = Stimulus( **arg )
        stim.data = data
        return stim
    load = staticmethod( load )

    def configure( self, modelLookup ):
        """Sanity check on all fields. First, check that all the entities
        named in experiment have counterparts in the model definition"""
        for i in self.entities:
            if not i in modelLookup:
                raise SimError( "Stim::configure: Error: object {} not defined in model lookup.".format( i ) )

Stimulus.argNames = ['timeUnits', 'quantityUnits', 'entities', 'field' ]

##########################################################################

class Readout:
    """Specifies readouts to be obtained from a specific component of 
    the model in the course of the simulated experiment. Almost always
    molecule quantity, but later might be electrical things like membrane 
    potential.
    There can be multiple readouts during an experiment.
    """
    ## Here are some static fields.
    epspFields = [ 'EPSP_peak', 'EPSP_slope', 'IPSP_peak', 'IPSP_slope' ]
    epscFields = [ 'EPSC_peak', 'EPSC_slope', 'IPSC_peak', 'IPSC_slope' ]
    fepspFields = [ 'fEPSP_peak','fEPSP_slope','fIPSP_peak','fIPSP_slope' ]
    elecFields = ['Vm', 'Im', 'current'] + epspFields + epscFields
    postSynFields = fepspFields + epspFields + epscFields
    def __init__( self,
            timeUnits = 's',
            quantityUnits = 'mM',
            useRatio = False,
            useNormalization=False,
            tabulateOutput = False,
            settleTime = 300.0,
            ratioReferenceEntities = '',
            ratioReferenceTime = 0.0,
            ratioReferenceDose = 0.0,
            ratioReferenceValue = 1.0,
            entities = '',
            field = '',     # Special fields EPSP_peak, EPSP_slope etc
            quantityScale = 1.0,    # Scaling from quantity units to SI
            useXlog = False,
            useYlog = False,
            scoringFormula = 'abs(1-(sim+1e-9)/(expt+1e-9))',
            data = []      # Data from experiment. rows of [t,val,stder]
            ):
        self.timeUnits = timeUnits
        """timeUnits may be us, ms, s, min, hours, days"""
        self.timeScale = next(v for k, v in convertTimeUnits.items() if timeUnits in k)
        """timeScale is timeUnits scaled to seconds"""
        self.quantityUnits = quantityUnits.strip()
        """Quantity Units may be: M, mM, uM, nM, pM, number, ratio, etc"""
        if self.quantityUnits in convertQuantityUnits:
            self.quantityScale = convertQuantityUnits[ self.quantityUnits ]
        else:
            raise SimError( "Readout::__init__: unknown quantity units '{}'".format( self.quantityUnits ) )

        if useXlog != "":    
            self.useXlog = str2bool(useXlog)
        else:
            self.useXlog = str2bool(useXlog)
        if useYlog != "":    
            self.useYlog = str2bool(useYlog)
        else:
            self.useYlog = str2bool(useYlog)
        self.useNormalization = str2bool(useNormalization)
        
        temp = entities.split( ',' )
        self.entities = [ i for i in temp if len(i) > 0 ]
        """Name of the model entity to read. Typically a molecule name,
        or the name of a compartment in an electrical model."""
        self.field = field
        """Name of the field/quantity associated with the entity. For
        example, conc for molecules, or Vm for a compartment."""
        self.settleTime = float( settleTime )
        """For dose response, we can specify how long to settle at 
        each level. A value of 0 or less means to automatically go 
        on till steady-state."""
        temp = ratioReferenceEntities.split( ',' )
        self.ratioReferenceEntities = [ i for i in temp if len(i) > 0 ]
        self.useRatio = (len( self.ratioReferenceEntities ) > 0)
        """Objects to use as reference for computing the readout ratio."""
        # ratioReferenceTime should really be a flag: ratioEachDose vs
        # ratioAtSpedifiedConc. We always run for settleTime.
        self.ratioReferenceTime = float( ratioReferenceTime )
        """Timepoint at which to sample the quantity to use as a reference for calculating the ratio. -1 means to sample reference each time we sample the readout, and to use the instantaneous ratio."""
        self.ratioReferenceDose = float( ratioReferenceDose )
        """Dose at which to sample the quantity to use as a reference for
        ratio calculations."""
        self.ratioReferenceValue = float( ratioReferenceValue )
        """The obtained reference value for scaling all simulation outputs. Defaults to 1."""
        self.data = data
        """Array of experimentally defined readout data. Each row has triplets of numbers, [time or dose, quantity, stderr]"""
        self.simData = [] 
        """Array of simulation results. One per data entry."""
        self.ratioData = [] 
        """Array of ratio results. One per data entry."""
        self.plots = []
        """List of continuous, fine-timeseries plots as numpy arrays, for readouts, only activated in single-run mode"""
        self.plotDt = 0.1   #Default dt for plots. Updated in sw::fillPlots
        self.epspFreq = 100.0 # Used to generate a single synaptic event
        self.epspWindow = 0.02 # Time of epspPlot to scan for peak/slope
        self.ex = 0.0005   # Electrode position for field recordings.
        self.ey = 0.0
        self.ez = 0.0
        self.fepspMin = -0.002 # 2 mm to the left of trode
        self.fepspMax = 0.001 # 1 mm to the right of trode
        
    def configure( self, modelLookup ):
        """Sanity check on all fields. First, check that all the entities
        named in experiment have counterparts in the model definition"""
        for i in self.entities:
            if not i in modelLookup:
                raise SimError( "Readout::configure: Error: object {} not defined in model lookup.".format( i ) )
        for i in self.ratioReferenceEntities:
            if not i in modelLookup:
                raise SimError( "Readout::configure: Error: ratioReferenceEntity '{}' not defined in model lookup.".format( i ) )

    def digestSteadyStateRun( self, ref, ret ):
        if len( self.ratioReferenceEntities ) > 0 and self.ratioReferenceTime >= 0.0: # Global reference readout
            assert( len( ret ) > 0 and len( ref ) > 0 )
            globalReference = ret.pop()
            ref = [globalReference] * len( ret )
        elif len( self.ratioReferenceEntities ) == 0:
            ref = [ self.quantityScale ] * len( ret )
        # The third case is that ratioReferenceTime < 0, in which case we
        # compute the ref for each stimulus value. That goes through 
        # unchanged.

        if self.useNormalization: # Another global reference; first pt
            ref = [ret[0]] * len( ret )

        # Check for zeroes in the denominator
        eps = 1e-16
        if len( [ x for x in ref if abs(x) < eps ] ) > 0:
            raise SimError( "runDoser: Normalization failed due to zero denominator" )
        # Finally assign the simData.
        self.simData = [ x/y for x, y in zip( ret, ref ) ]


    def displayPlots( self, fname, modelLookup, stim, hideSubplots, exptType ):
        if "doseresponse" in exptType:
            for i in stim.entities:
                elms = modelLookup[i]
                for j in elms:
                    pp = PlotPanel( self, exptType, xlabel = j.name +'('+stim.quantityUnits+')' )
                    pp.plotme( fname, pp.ylabel, joinSimPoints = True )
        elif "barchart" in exptType:
            for i in self.entities:
                elms = modelLookup[i]
                for j in elms:
                    pp = PlotPanel( self, exptType, xlabel = j.name +'('+stim.quantityUnits+')' )
                    pp.plotbar( self, stim, fname )
        elif "timeseries" in exptType:
            tsUnits = self.quantityUnits
            if self.field in Readout.epspFields:
                tsUnits = 'mV'
            elif self.field in Readout.epscFields:
                tsUnits = 'pA'
            elif self.field in Readout.fepspFields:
                if not hideSubplots:
                    self.plotFepsps( fname )
                    return
            elif self.useNormalization:
                tsUnits = 'Fold change'
            tsScale = convertQuantityUnits[tsUnits]

            ######################################
            pp = PlotPanel( self, exptType )
            assert( len( self.plots ) > 0)
            numPts = len( self.plots[0] )
            assert( numPts > 0 )
            sumvec = np.zeros( numPts )
            if len( self.ratioData ) > 0:
                scale = tsScale * self.ratioData[0]
            else:
                scale = tsScale * self.ratioReferenceValue

            for ypts in self.plots:
                tconv = next( v for k, v in convertTimeUnits.items() if self.timeUnits in k )
                xpts = np.array( range( numPts)  ) * self.plotDt / tconv
                ypts /= scale
                sumvec += ypts
                if not hideSubplots:
                    # Plot summed components. Need to access name.
                    #pylab.plot( xpts, ypts, 'r:', label = j.name )
                    pylab.plot( xpts, ypts, 'r:' )
            pylab.plot( xpts, sumvec, 'r--' )
            ylabel = pp.ylabel
            if self.field in ( Readout.epspFields + Readout.epscFields ):
                if self.field in Readout.epspFields:
                    pylab.ylabel( '{} Vm ({})'.format( self.entities[0], tsUnits ) )
                else:
                    pylab.ylabel( '{} holding current ({})'.format( self.entities[0], tsUnits ) )

                pylab.figure(2)
                if self.useNormalization:
                    ylabel = '{} Fold change'.format( self.field )
            pp.plotme( fname, ylabel )

            ######################################
            '''
            for i in self.entities:
                elms = modelLookup[i]
                ypts = self.plots[elms[0].name].vector
                numPts = len( ypts )
                if numPts > 0:
                    tconv = next( v for k, v in convertTimeUnits.items() if self.timeUnits in k )
                    xpts = np.array( range( numPts)  ) * self.plots[elms[0].name].dt / tconv
                sumvec = np.zeros(len(xpts))
                for j in elms:
                    pp = PlotPanel( self, exptType )
                # Here we plot the fine timeseries for the sim.
                # Not yet working for all options of ratio.
                    if len( self.ratioData ) > 0:
                        scale = tsScale * self.ratioData[0]
                    else:
                        scale = tsScale
                    ypts = self.plots[j.name].vector / scale
                    sumvec += ypts
                    if (not hideSubplots) and (len( elms ) > 1): 
                        # Plot summed components
                        pylab.plot( xpts, ypts, 'r:', label = j.name )

                pylab.plot( xpts, sumvec, 'r--' )
                ylabel = pp.ylabel
                if self.field in ( Readout.epspFields + Readout.epscFields ):
                    if self.field in Readout.epspFields:
                        pylab.ylabel( '{} Vm ({})'.format( self.entities[0], tsUnits ) )
                    else:
                        pylab.ylabel( '{} holding current ({})'.format( self.entities[0], tsUnits ) )

                    pylab.figure(2)
                    if self.useNormalization:
                        ylabel = '{} Fold change'.format( self.field )
                pp.plotme( fname, ylabel )
            '''

    def plotFepsps( self, fname ):
        tconv = next( v for k, v in convertTimeUnits.items() if self.timeUnits in k )
        assert( len( self.plots ) > 0 )
        numPts = len( self.plots[0] )
        xpts = np.array( range( numPts)  ) * self.plotDt / tconv
        sumvec = np.zeros( numPts )
        for i, wt in zip( self.plots, self.wts ):
            # I'm going to plot the original currents rather than the
            # variously scaled contributions leading up to the fEPSP
            ypts = i * 1e12   # Hack, hard code currents in pA
            pylab.plot( xpts, ypts, 'r:' )
            sumvec += ypts
        pylab.plot( xpts, sumvec, 'r--' )
        pylab.xlabel( "time ({})".format( self.timeUnits) )
        pylab.ylabel( "Compartment currents Im (pA)" )
        pylab.figure(2)
        pp = PlotPanel( self, "timeseries" )
        pp.plotme( fname, "fEPSP (mV)" )

    def doScore( self, scoringFormula ):
        #assert( len(self.data) == len( self.simData ) )
        score = 0.0
        numScore = 0.0
        dvals = [i[1] for i in self.data]
        datarange = max( dvals ) - min( dvals )
        if self.tabulateOutput:
            print( "{:>12s}   {:>12s}  {:>12s}  {:>12s}".format( "t", "expt", "sim", "sem" ) )
        for i,sim in zip( self.data, self.simData ):
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

    def directParamScore( readouts, modelLookup, scoringFormula ):
        score = 0.0
        numScore = 0.0
        for rd in readouts:
            for d in rd.data:
                entity = d[0]
                expt = d[1]*rd.quantityScale
                sem = d[2]*rd.quantityScale
                sim = sw.getObjParam( entity, rd.field )
                #sim = elmList[0].getField( rd.field )
                score += eval( scoringFormula )
                numScore += 1.0
                #print( entity, rd.field, sim, expt, sem, score, numScore, "\n" )
        #print( "direct score of {}".format( score / numScore ) )
        if numScore == 0:
            return -1
        return score/numScore
    directParamScore = staticmethod( directParamScore )

    def load( fd ):
        arg, data, param, struct, modelLookup = innerLoad( fd, Readout.argNames, dataWidth = 3 )
        # Data is either time, value, stderr or entity, value, stderr
        readout = Readout( **arg )
        readout.data = data
        return readout
    load = staticmethod( load )

Readout.argNames = ['timeUnits', 'quantityUnits', 
        'useXlog', 'useYlog', 'useNormalization', 
        'entities', 'field', 'settleTime', 'ratioReferenceTime', 
        'ratioReferenceDose','ratioReferenceEntities']

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
    def __init__( self,
            modelSource = 'paper',  # Options are paper, inHouse, database
            citation = '',  # Journal name/ in-house project name/ database
            citationId = '',    # PMID/Lab note reference/accession number
            authors = '',   # Who did the work
            detail = '',    # Figure number etc. to pin it down.
            modelSubset = 'all',    # Define a model subset to use.
            fileName = '',  # Specify model file name
            solver = 'gsl', # What solver to use for calculations
            notes = '',     # Curator notes.
            ignoreMissingObj = False,   # Flag for cases where we may have 
                                        # lookups for items not in model,
                                        # such as a reduced model.
            itemstodelete = [], # topology change
            stimulusMolecules = [], # stimulusMolecules with in model mapped to stumuli's molecules
            readoutMolecules = [],  # readoutsMolecules with in model mapped to readouts's molecules
            referenceMolecule = [], # reference molecules with in model mapped to readout's referenceMolecules
            scoringFormula = 'abs(1-(sim+1e-9)/(expt+1e-9))',
            parameterChange = [] # Param of model to change at run start.

    ):
        self.modelSource = modelSource
        self.citation = citation
        self.citationId = citationId
        self.authors = authors
        self.detail = detail
        self.modelSubset = modelSubset
        self.fileName = fileName
        self.solver = solver
        self.notes = notes
        self.parameterChange = []
        self.itemstodelete = []
        self.scoringFormula = scoringFormula
        #self.fieldLookup = {'nInit':'nInit','n':'n','conc':'conc','concInit':'concInit','Iclamp':'inject','Vclamp':'inject','Vm':'Vm','Im':'Im'

    def load( fd ):
        '''
        Model::load builds a model instance from a file and returns it.
        '''
        arg, data, param, struct, modelLookup = innerLoad( fd, Model.argNames )
        
        model = Model( **arg )
        for i in param:
            model.addParameterChange( i[0], i[1], i[2] )
        for j in struct[:]:
            model.addStructuralChange(j.lstrip(),"delete")
        model._tempModelLookup = modelLookup
        #model.fieldLookup = fieldLookup
        return model

    load = staticmethod( load )


    def addParameterChange( self, entity, field, data ):
        '''
        Model::addParameterChange adds a modification of parameter values
        to be applied to the model.
        At present the system assumes that this can only be done before the
        simulation starts.
        '''
        self.parameterChange.append( ( entity, field, data ) )


    def addStructuralChange( self, entity, change ):
        '''
        Model::addStructuralChange causes a topology change to the model,
        typically deleting model entities. 
        Later possibly something clever like adding a tracer.
        At present the system assumes that this can only be done before the
        simulation starts.
        '''
        if entity:
            entity = entity.replace('\'',"")
            entity = entity.replace('\"',"")
            entity = entity.replace('\n',"")
            entity = entity.replace('',"")

        self.itemstodelete.append((entity,change))

    # Exported to simWrap: _scaleParams, deleteItems, subsetItems
    # Exported to simWrapMoose: findObj, scaleOneParam

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
        sw.deleteItems( self.itemstodelete )
        if not( self.modelSubset.lower() == 'all' or self.modelSubset.lower() == 'any' ):
            sw.subsetItems( self.modelSubset )

        #Function call for checking dangling Reaction/Enzyme/Function's
        sw.pruneDanglingObj( erSPlist)
        sw.changeParams( self.parameterChange )

            
Model.argNames = ['modelSource', 'citation', 'citationId', 'authors',
            'modelSubset', 'fileName', 'solver', 'notes' ,'scoringFormula','itemstodelete','parameterChange']

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
def list_to_dict(rlist):
    return dict(map(lambda s : s.split(':'), rlist))

def innerLoad( fd, argNames, dataWidth = 2):
    data = []
    param = []  # list of tuples of objname, field, value.
    arg = {}
    struct = []
    modelLookup = {}
    #fieldLookup = {}
    for line in fd:
        cols = line.split( "\t" )
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            return arg, data, param, struct, modelLookup

        c0 = cols[0].strip()
        if keywordMatches( c0, 'modelLookup' ):
            # Lines of the form exptName1:simName1,exptName2:simName2,...
            if cols[1] != "":
                temp = cols[1].split( ',' )
                modelLookup = { i.split(':')[0]:i.split(':')[1].strip() for i in temp }

        if keywordMatches( c0, 'Data' ):
            readData( fd, data, dataWidth )
            return arg, data, param, struct, modelLookup

        for i in argNames:
            if keywordMatches( c0, i ):
                arg[i] = str.strip( nonBlank( cols) )
                continue
        if keywordMatches(c0,"parameterChange"):
            readParameter(fd,param,dataWidth)

        if keywordMatches( c0, 'itemstodelete' ):
            struct= cols[1].split(',')

    return arg, data, param, struct, modelLookup

def nonBlank( cols ):
    for i in cols[1:]:
        if i != '':
            return i
    return ''

def readData( fd, data, width ):
    entityNameInFirstCol = False
    for line in fd:
        if line[0] == '#':
            continue
        cols = line.split("\t" )
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            break
        cl = cols[0].strip().lower()
        if cl == "time" or cl == "dose" or cl == "settletime" or cl == 'entity':
            if cl == 'entity':
                entityNameInFirstCol = True
            continue
        row = []
        for i in range( len( cols ) ):
            if cols[i] != '':
                if i == 0 and entityNameInFirstCol:
                    row.append( cols[i] )
                else:
                    row.append( float( cols[i] ) )
                if len( row ) >= width:
                    break;
        if len( row ) > 0 and len( row ) < width:
            row.append( 0.0 )
        data.append( row )

def readParameter(fd, para, width):
    for line in fd:
        cols = line.split("\t")
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            break
        if cols[0].strip().lower() == "object":
            continue
        row = []
        lcols = 0
        for c in cols:
            c = c.replace('\n',"")
            if c != '':
                if lcols > 1 :
                    row.append(float(c))
                else:
                    row.append(c)
                if len( row ) > width:
                    break;
                lcols = lcols+1
        para.append( row )

def str2bool( arg ):
    if arg == False or arg == 0:
        return False
    if arg.lower() == 'false' or arg == '0':
        return False
    return True

##########################################################################
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
    for i in readouts:
        if i.field in Readout.postSynFields:
            for j in range( len( i.data ) ):
                t = float( i.data[j][0] ) * i.timeScale
                heapq.heappush( q, Qentry(t, pauseHsolve, 1) ) # Turn on hsolve
                heapq.heappush( q, Qentry(t, i.stim, i.epspFreq) )
                heapq.heappush( q, Qentry(t+1.0/i.epspFreq, i.stim, 0) )
                heapq.heappush( q, Qentry(t+i.epspWindow, i, j) )# Measure after EPSP
                heapq.heappush( q, Qentry(t+i.epspWindow+pauseHsolve.epspSettle, pauseHsolve, 0) )

        else:
            # We push in the index of the data entry so the readout can
            # process it when it is run. It will grab both the readout and
            # ratio reference if needed.
            for j in range( len( i.data ) ):
                t = float( i.data[j][0] ) * i.timeScale
                heapq.heappush( q, Qentry(t, i, j) )

        if i.useRatio and i.ratioReferenceTime >= 0.0:
            # We push in -1 to signify that this is to get ratio reference
            heapq.heappush( q, Qentry(float(i.ratioReferenceTime)*i.timeScale, i, -1) )


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
    #print( "########## val = {}".format( val ) )
    if readout.field in (Readout.epspFields + Readout.epscFields):
        readout.plots, readout.plotDt = sw.fillPlots()
        doEpspReadout( readout )
    elif readout.field in Readout.fepspFields:
        readout.plots, readout.plotDt = sw.fillPlots()
        doFepspReadout( readout )
    elif val == -1: # This is a special event to get RatioReferenceValue
        readout.ratioReferenceValue = sw.sumFields( readout.ratioReferenceEntities, readout.field )
        #print(">>>>>>>>>>>> {}, {}.{}, qtime = {}".format( readout.ratioReferenceValue, readout.ratioReferenceEntities, readout.field, qe.t ) )
        #readout.simData = [ s/ratioReference for s in readout.simData ] 
        #readout.ratioData.append( ratioReference )
        #print("SIMDATA: {}".format( readout.simData ))
        #print("RatioDATA {}".format( readout.ratioData ))
    else:
        doEntityAndRatioReadout(readout, readout.field)

def doFepspReadout( readout ):
    n = int( round( readout.epspWindow / readout.plotDt ) )
    #n = int( round( readout.epspWindow / readout.epspPlot.dt ) )
    assert( n > 5 )
    assert( len( readout.plots ) == len( readout.wts ) )
    pts = np.zeros( n )
    #numPlots = len( readout.epspPlot.vec )
    #assert( numPlots == len( readout.wts ) )
    #for i, wt in zip( readout.epspPlot.vec, readout.wts ):
    #    pts += np.array( i.vector[-n:] ) * wt
    for i, wt in zip( readout.plots, readout.wts ):
        pts += i[-n:] * wt
    #pts = np.array( readout.epspPlot.vector[-n:] )
    #pts /= len( readout.epspPlot.vec )
    pts /= len( readout.wts )
    #print( "DOING EPSP READOUT WITH " +  readout.field )
    #print( ["{:.3g} ".format( x ) for x in pts] )
    if "slope" in readout.field:
        dpts = pts[1:] - pts[:-1]
        slope = max( abs( dpts ) )/readout.plotDt
        readout.simData.append( slope / readout.quantityScale )
    elif "peak" in readout.field:
        pts -= pts[0]
        pk = max( abs(pts) )
        readout.simData.append( pk / readout.quantityScale )

def doEpspReadout( readout ):
    n = int( round( readout.epspWindow / readout.plotDt ) )
    assert( n > 5 )
    assert( len( readout.plots ) > 0 )
    assert( len( readout.plots[0] ) > 5 )
    pts = readout.plots[0][-n:]
    #pts = np.array( readout.epspPlot.vector[-n:] )
    #print( "DOING EPSP READOUT WITH " +  readout.field )
    #print( ["{:.3g} ".format( x ) for x in pts] )
    if "slope" in readout.field:
        dpts = pts[1:] - pts[:-1]
        slope = max( abs( dpts ) )/readout.plotDt
        readout.simData.append( slope / readout.quantityScale )
    elif "peak" in readout.field:
        pts -= pts[0]
        pk = max( abs(pts) )
        readout.simData.append( pk / readout.quantityScale )
    if readout.useNormalization and len( readout.simData) == 1:
         readout.ratioReferenceValue = readout.simData[0]

def doEntityAndRatioReadout( readout, field ):
    sim = sw.sumFields( readout.entities, field )
    readout.simData.append( sim/readout.quantityScale )
    ratioReference = 0.0
    if readout.ratioReferenceTime < 0.0 :
        ratioReference = sw.sumFields( readout.ratioReferenceEntities, field )
        readout.ratioData.append( ratioReference )

def doSynInputReadout( readout, modelLookup, field ):
    readout.simData.append( 0 )

def processReadouts( readouts, scoringFormula ):
    numScore  = 0
    score = 0.0
    for i in readouts:
        score += i.doScore( scoringFormula )
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
        elif isinstance( qe.entry, Readout ):
            doReadout( qe, model )
        elif isinstance( qe.entry, PauseHsolve ):
            qe.entry.setHsolveState( int(qe.val) )

    for i in readouts:
        # Normalize. Applies to cases where we do a special run for a 
        # single normalization value that scales all points. Since it
        # defaults to 1, we can simply apply always.
        i.simData = [ x/i.ratioReferenceValue for x in i.simData ]
        # Collect detailed time series
        i.plots, i.plotDt = sw.fillPlots()
    score = processReadouts( readouts, model.scoringFormula )

    return score


##########################################################################
def parseAndRunDoser( model, stims, readouts ):
    if len( stims ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs \
            exactly one stimulus block, {} defined".format( len(stims)) )
    if len( readouts ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs \
            exactly one readout block, {} defined".format( len(readout) ) )
    numLevels = len( readouts[0].data )
    
    if numLevels == 0:
        raise SimError( "parseAndRunDoser: no dose (stimulus) levels defined for run" )
    
    runTime = readouts[0].settleTime
    
    if runTime <= 0.0:
        print( "Currently unable to handle automatic settling to stead-state in doseResponse, using default 300 s." )
        runTime = 300
    
    doseMol = ""
    #Stimulus Molecules
    #Assuming one stimulus block, one molecule allowed
    runDoser( model, stims[0], readouts[0] )
    score = processReadouts( readouts, model.scoringFormula )
    return score

def runDoser( model, stim, readout ):
    stimList = []
    responseList = []
    for dose, response, sem in readout.data:
        stimList.append( [ (stim.entities[0], stim.field, dose, stim.quantityScale), ] )
    if len( readout.ratioReferenceEntities ) > 0 and readout.ratioReferenceTime >= 0.0:
        # Add another entry for the global reference readout.
        stimList.append( [ (stim.entities[0], stim.field, readout.ratioReferenceDose, stim.quantityScale), ] )
    responseList = [ readout.entities, readout.field, readout.ratioReferenceEntities, readout.field ]
    ret, ref = sw.steadyStateStims( stimList, responseList, isSeries = True, settleTime = readout.settleTime )

    readout.digestSteadyStateRun( ref, ret )
    # and here we go about extracting the values from ret and ref.

##########################################################################

def runBarChart( model, stim, readout ):
    ''' The bar chart is set up by having a series of stim values as
    entity,value pairs in stim.data
    Then the Readouts data has a series of values of the form
    flags   value   stderr
    where the flags are strings of the form "101" or "+-+"
    to indicate which of the stim-value pairs should be applied.
    '''

    stimSource = []
    stimList = []
    responseList = []
    for entity, value in stim.data:
        stimEntry = ( entity, stim.field, value, stim.quantityScale )
        stimSource.append( stimEntry ) 
    for flags, response, sem in readout.data:
        stimLine = []
        for i in range( len( flags ) ):
            if flags[i] == '1' or flags[i] == '+':
                stimLine.append( stimSource[i] )
        stimList.append( stimLine )
    # Add a normalizing reference. This is a bit patchy. Here we assume
    # that the reference is for the case where there are no stims.
    if readout.useRatio and readout.ratioReferenceTime >= 0.0:
        #stimList.append( [(readout.ratioReferenceEntities[0], stim.field, readout.ratioReferenceDose, stim.quantityScale), ] )
        stimList.append( [] )

    responseList = [ readout.entities, readout.field, readout.ratioReferenceEntities, readout.field ]
    # And here we go:
    ret, ref = sw.steadyStateStims( stimList, responseList, isSeries = False, settleTime = readout.settleTime )
    # Extract values.
    readout.digestSteadyStateRun( ref, ret )

def parseAndRunBarChart( model, stims, readouts ):
    if len( stims ) != 1:
        raise SimError( "parseAndRunBarChart: BarChart run needs exactly \
            one stimulus block, {} defined".format( len( stims ) ) )
    if len( readouts ) != 1:
        raise SimError( "parseAndRunBarChart: BarChart run needs exactly \
            one readout block, {} defined".format( len( readout ) ) )
    numLevels = len( readouts[0].data )
    
    if numLevels == 0:
        raise SimError( "parseAndRunBarChart: no stimulus levels defined for run" )
    
    runTime = readouts[0].settleTime
    
    if runTime <= 0.0:
        print( "Currently unable to handle automatic settling to steady-state in Bar Charts, using default 300 s." )
        runTime = 300

    runBarChart( model, stims[0], readouts[0] )

    score = processReadouts( readouts, model.scoringFormula )
    return score

##########################################################################

class PlotPanel:
    def __init__( self, readout, exptType, xlabel = '' ):
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

        self.xpts = [ i[0] for i in readout.data]
        self.sim = readout.simData # Ratios already handled at this stage
        self.expt = [ i[1] for i in readout.data]
        self.yerror = [ i[2] for i in readout.data]
        self.sumName=""
        for i in self.name:
            self.sumName += i
            self.sumName += " "
            self.ylabel = '{} {} ({})'.format(i, readout.field, readout.quantityUnits ) #problem here.check so that y-axis are for diff plts not in one plot

    def convertBarChartLabels( self, readout, stim ):
        ret = []
        doseMol = [ i[0] for i in stim.data ]
        for i in readout.data:
            ticklabel = ""
            for j in range( len( i[0] ) ):
                if i[0][j] == '1' or i[0][j] == '+':
                    ticklabel += doseMol[j] + '\n'
                else:
                    ticklabel += '-\n'
            ret.append( ticklabel )
        return ret


    def plotbar( self, readout, stim, scriptName ):
        barpos = np.arange( len( self.sim ) )
        width = 0.35 # A reasonable looking bar width
        exptBar = pylab.bar(barpos - width/2, self.expt, width, yerr=self.yerror, color='SkyBlue', label='Experiment')
        simBar = pylab.bar(barpos + width/2, self.sim, width, color='IndianRed', label='Simulation')
        pylab.xlabel( "Stimulus combinations" )
        pylab.ylabel( self.ylabel )
        pylab.title(scriptName)
        pylab.legend(fontsize="small",loc="upper left")
        ticklabels = [ i[0] + '\n' for i in readout.data ] 
        assert len( ticklabels ) == len( barpos )
        ticklabels = self.convertBarChartLabels( readout, stim )
        pylab.xticks(barpos, ticklabels )

    def plotme( self, scriptName, ylabel, joinSimPoints = False ):
        sp = 'ro-' if joinSimPoints else 'ro'
        if self.useXlog:
            if self.useYlog:
                pylab.loglog( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                pylab.loglog( self.xpts, self.sim, sp, label = 'sim', linewidth='2' )
            else:
                pylab.semilogx( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                pylab.semilogx( self.xpts, self.sim, sp, label = 'sim', linewidth='2' )
        else:
            if self.useYlog:
                pylab.semilogy( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                pylab.semilogy( self.xpts, self.sim, sp, label = 'sim', linewidth='2' )
            else:
                pylab.plot( self.xpts, self.expt,'bo-', label = 'experiment', linewidth='2' )
                pylab.errorbar( self.xpts, self.expt, yerr=self.yerror )
                pylab.plot( self.xpts, self.sim, sp, label = 'sim', linewidth='2' )

        pylab.xlabel( self.xlabel )
        pylab.ylabel( ylabel )
        pylab.title(scriptName)
        pylab.legend(fontsize="small",loc="lower right")

########################################################################
def loadTsv( fname ):
    stims = []
    readouts = []
    fs = fname.split('.')
    if len(fs) < 2:
        if fs[-1] != 'tsv':
            raise SimError( " file '" + fname + "' should end in .tsv" )
    with open( fname ) as fd:
        for line in fd:
            if len( line ) > 1 and line[0] != '#':
                cols = line.split('\t')
                if len( cols ) > 0:
                    c0 = cols[0].strip()
                    if c0 == 'Experiment metadata':
                        expt = Experiment.load(fd )
                    if c0 == 'Stimuli':
                        stims.append( Stimulus.load(fd ) )
                    if c0 == 'Readouts':
                        readouts.append( Readout.load(fd) )
                    if c0 == 'Model mapping':
                        model = Model.load(fd )
    return expt, stims, readouts, model

def runit( expt, model, stims, readouts ):
    for i in stims:
        i.configure( model._tempModelLookup )
    for i in readouts:
        i.configure( model._tempModelLookup )

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

    parser.add_argument( 'script', type = str, help='Required: filename of experiment spec, in tsv format.')
    parser.add_argument( '-m', '--model', type = str, help='Optional: model filename, .g or .xml', default = "" )
    parser.add_argument( '-d', '--dump_subset', type = str, help='Optional: dump selected subset of model into named file', default = "" )
    parser.add_argument( '-p', '--param_file', type = str, help='Optional: Generate file of tweakable params belonging to selected subset of model', default = "" )
    parser.add_argument( '-t', '--tabulate_output', action="store_true", help='Flag: Print table of plot values. Default is NOT to print table' )
    parser.add_argument( '-hp', '--hide_plot', action="store_true", help='Hide plot output of simulation along with expected values. Default is to show plot.' )
    parser.add_argument( '-hs', '--hide_subplots', action="store_true", help='Hide subplot output of simulation. By default the graphs include dotted lines to indicate individual quantities (e.g., states of a molecule) that are being summed to give a total response. This flag turns off just those dotted lines, while leaving the main plot intact.' )
    parser.add_argument( '-o', '--optimize_elec', action="store_true", help='Optimize electrical computation. By default the electrical computation runs for the entire duration of the simulation. With this flag the system turns off the electrical engine except during the times when electrical stimuli are being given. This can be *much* faster.' )
    parser.add_argument( '-s', '--scale_param', nargs=3, default=[],  help='Scale specified object.field by ratio.' )
    parser.add_argument( '-settle_time', '--settle_time', type=float, default=0,  help='Run model for specified settle time and return dict of {path,conc}.' )
    parser.add_argument( '-imo', '--ignore_missing_obj', action="store_true", help='Flag, default False. When set the code ignores references to missing objects. Normally it would throw an error.' )
    args = parser.parse_args()
    innerMain( args.script, modelFile = args.model, dumpFname = args.dump_subset, paramFname = args.param_file, hidePlot = args.hide_plot, hideSubplots = args.hide_subplots, optimizeElec = args.optimize_elec, scaleParam = args.scale_param, settleTime = args.settle_time, tabulateOutput = args.tabulate_output, ignoreMissingObj = args.ignore_missing_obj )


def innerMain( script, modelFile = "model/synSynth7.g", dumpFname = "", paramFname = "", hidePlot = True, hideSubplots = False, optimizeElec=True, silent = False, scaleParam=[], settleTime = 0, settleDict = {}, tabulateOutput = False, ignoreMissingObj = False, simWrap = "" ):
    ''' If *settleTime* > 0, then we need to return a dict of concs of
    all variable pools in the chem model obtained after loading in model, 
    applying all modifications, and running for specified settle time.\n
    If the *settleDict* is not empty, then the system goes through and 
    matches up pools to assign initial concentrations.
    '''

    global pause
    global sw
    if simWrap == "":
        sw = simWrapMoose.SimWrapMoose( ignoreMissingObj = ignoreMissingObj )
    else:
        sw = simWrap.SimWrap( ignoreMissingObj = ignoreMissingObj )
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    modelWarning = ""
    expt, stims, readouts, model = loadTsv( script )
    #model.ignoreMissingObj = ignoreMissingObj
    for r in readouts:
        r.tabulateOutput = tabulateOutput

    if modelFile != "":
        model.fileName = modelFile
    model.pauseHsolve = PauseHsolve( optimizeElec )
    # First we load in the model using EE so it is easier to tweak
    try:
        if not os.path.isfile(model.fileName):
            raise SimError( "Model file name {} not found".format( model.fileName ) )
        fileName, file_extension = os.path.splitext(model.fileName)
        sw.loadModelFile( model.fileName, model.modify, scaleParam, dumpFname, paramFname, model._tempModelLookup )

        if expt.exptType == 'directparameter':
            score = Readout.directParamScore( readouts, model._tempModelLookup, model.scoringFormula )
            if not hidePlot:
                print( "Score = {:.3f} for\t{}\tElapsed Time = 0.0 s".format( score, os.path.basename(script) ) )
            sw.deleteSimulation()
            return score

        hasVclamp = False
        readoutStim = stims[0]
        for i in stims:
            if i.field.lower() == 'vclamp':
                hasVclamp = True
                vpath = sw.buildVclamp( i )
                model._tempModelLookup['vclamp'] = vpath
            elif i.field.lower() == 'inject':
                readoutStim = i
            if len(i.entities) > 0 and i.entities[0].lower() == 'syninput':
                readoutStim = i
        if readouts[0].field in Readout.postSynFields:
            readouts[0].stim = readoutStim 
        sw.makeReadoutPlots( readouts )
        sw.buildSolver( model.solver, useVclamp = hasVclamp )
        ##############################################################
        # Here we handle presettling. First to generate, then to apply
        # the dict of settled values.
        if settleTime > 0:
            return sw.presettle( settleTime )

        sw.assignPresettle( settleDict )
        ##############################################################

        t0 = time.time()
        score = runit( expt, model,stims, readouts  )
        elapsedTime = time.time() - t0
        if not hidePlot:
            print( "Score = {:.3f} for\t{}\tElapsed Time = {:.1f} s".format( score, os.path.basename(script), elapsedTime ) )
            for i in readouts:
                pylab.figure(1)
                i.displayPlots( script, sw.modelLookup, stims[0], hideSubplots, expt.exptType )
                
            pylab.show()
        sw.deleteSimulation()
        return score
        
    except SimError as msg:
        if not silent:
            print( "Error: findSim failed for script {}: {}".format(script, msg ))
        sw.deleteSimulation
        if __name__ == '__main__':
            traceback.print_exc()
        return -1.0
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
