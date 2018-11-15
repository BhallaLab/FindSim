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
import argparse
import moose
import os
import re
import ntpath
import time
import imp      # This is apparently deprecated in Python 3.4 and up
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

epspFields = [ 'EPSP_peak', 'EPSP_slope', 'IPSP_peak', 'IPSP_slope' ]
epscFields = [ 'EPSC_peak', 'EPSC_slope', 'IPSC_peak', 'IPSC_slope' ]

elecFields = ['Vm', 'Im', 'current'] + epspFields + epscFields
elecDt = 50e-6
elecPlotDt = 100e-6


def keywordMatches( k, m ):
    return k.lower() == m.lower()

class SimError( Exception ):
    def __init__( self, value ):
        self.value = value
    def __str__( self ):
        return repr( self.value )

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
    def __init__( self,
            timeUnits = 's',
            quantityUnits = 'mM',
            useRatio = False,
            useNormalization=False,
            settleTime = 300.0,
            ratioReferenceEntities = '',
            ratioReferenceTime = 0.0,
            ratioReferenceDose = 0.0,
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
        self._simDataReference = 1.0
        
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
        self.ratioReferenceTime = float( ratioReferenceTime )
        """Timepoint at which to sample the quantity to use as a reference for calculating the ratio. -1 means to sample reference each time we sample the readout, and to use the instantaneous ratio."""
        self.ratioReferenceDose = float( ratioReferenceDose )
        """Dose at which to sample the quantity to use as a reference for
        ratio calculations."""
        self.data = data
        """Array of experimentally defined readout data. Each row has triplets of numbers, [time or dose, quantity, stderr]"""
        self.simData = [] 
        """Array of simulation results. One per data entry."""
        self.ratioData = [] 
        """Array of ratio results. One per data entry."""
        self.plots = {}
        """Dict of continuous, fine-timeseries plots for readouts, only activated in single-run mode"""
        self.epspFreq = 100.0 # Used to generate a single synaptic event
        self.epspWindow = 0.02 # Time of epspPlot to scan for peak/slope
        
    def configure( self, modelLookup ):
        """Sanity check on all fields. First, check that all the entities
        named in experiment have counterparts in the model definition"""
        for i in self.entities:
            if not i in modelLookup:
                raise SimError( "Readout::configure: Error: object {} not defined in model lookup.".format( i ) )
        for i in self.ratioReferenceEntities:
            if not i in modelLookup:
                raise SimError( "Readout::configure: Error: ratioReferenceEntity '{}' not defined in model lookup.".format( i ) )

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
            if self.field in epspFields:
                tsUnits = 'mV'
            elif self.field in epscFields:
                tsUnits = 'pA'
            elif self.useNormalization and abs(self._simDataReference)>1e-15:
                tsUnits = 'Fold change'
            tsScale = convertQuantityUnits[tsUnits]
            #print( "tsScale = {}, {}".format( tsScale, tsUnits ) )

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
                    #print( "LEN(ratioData) = {}, quantScale={}, simDataReference={}".format( len(self.ratioData), self.quantityScale,self._simDataReference ) )
                    #print( "plotvec name = {}, val= {}".format( j.name, self.plots[j.name].vector ) )
                    ypts = self.plots[j.name].vector / scale
                    sumvec += ypts
                    if (not hideSubplots) and (len( elms ) > 1): 
                        # Plot summed components
                        pylab.plot( xpts, ypts, 'r:', label = j.name )

                pylab.plot( xpts, sumvec, 'r--' )
                ylabel = pp.ylabel
                if self.field in ( epspFields + epscFields ):
                    if self.field in ( epspFields  ):
                        pylab.ylabel( '{} Vm ({})'.format( self.entities[0], tsUnits ) )
                    else:
                        pylab.ylabel( '{} holding current ({})'.format( self.entities[0], tsUnits ) )

                    pylab.figure(2)
                    if self.useNormalization:
                        ylabel = '{} Fold change'.format( self.field )
                pp.plotme( fname, ylabel )

    def applyRatio( self ):
        eps = 1e-16
        rd = self.ratioData
        if len(rd) == 0:
            rd = [1.0]*len(self.data)
        elif len(rd) == 1:
            rd = [rd[0]]*len(self.data)
        assert( len(rd) == len( self.data ) )
        rd = [ 1.0 if abs(x) < eps else x for x in rd ] # eliminate div/0.0

        if self.useNormalization:
            if abs(self.simData[0]) < eps:
                raise SimError( "applyRatio: Normalization failed because abs(simData[0]) {} ~= zero".format( self.simData[0] ) )
            normalization = self.simData[0] / rd[0]
            self._simDataReference = normalization
        else:
            normalization = self.quantityScale
        
        self.simData = [ s/(r * normalization) for s, r in zip( self.simData, rd ) ]

    def doScore( self, scoringFormula ):
        assert( len(self.data) == len( self.simData ) )
        score = 0.0
        numScore = 0.0
        dvals = [i[1] for i in self.data]
        datarange = max( dvals ) - min( dvals )
        for i,sim in zip( self.data, self.simData ):
            t = i[0]
            expt = i[1]
            sem = i[2]
            #print t, expt, sem, sim, datarange
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
                if not entity in modelLookup:
                    raise SimError( "Readout::directParamScore: Entity {} not found".format( entity ) )
                elmList = modelLookup[entity]
                if len( elmList ) != 1:
                    raise SimError( "Readout::directParamScore: Should only have 1 object, found {} ".format( len( elmList ) ) )
                # We use a utility function because findSim may permit
                # parameters like Kd that need to be evaluated.
                sim = getObjParam( elmList[0], rd.field )
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
        self.modelLookup = {}
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
            #model.addStructuralChange( i[0], i[1] )
            model.addStructuralChange(j.lstrip(),"delete")
        model._tempModelLookup = modelLookup
        #model.fieldLookup = fieldLookup
        return model

    load = staticmethod( load )

    def buildModelLookup( self ):
        for i in self._tempModelLookup:
            paths = self._tempModelLookup[i].split('+')
            # Summed sim entities are separated with a '+', but map to a 
            # single experimentally defined entity.
            #print( "In buildModelLookup, seeking {}:{}".format( i, paths[0] ) )
            foundObj = [ self.findObj( '/model', p) for p in paths ]
            self.modelLookup[i] = foundObj

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

    def findObj( self,rootpath, name, noRaise = False ):
        '''
        Model:: findObj locates objects uniquely specified by a string. 
        The object can be located at any depth in the model tree.
        The identifier string typically consists of the name of an object,
        but it may be necessary to disambiguate it by including its parent
        name as well.
        For example, if there is a foo/bar and a zod/bar, then we will 
        have to pass "zod/bar" to uniquely specify the object.
        '''
        try1 = moose.wildcardFind( rootpath+'/' + name )
        try2 = moose.wildcardFind( rootpath+'/##/' + name )
        try2 = [ i for i in try2 if not '/model[0]/plots[0]' in i.path ]  
        if len( try1 ) + len( try2 ) > 1:
            raise SimError( "findObj: ambiguous name: '{}'".format(name) )
        if len( try1 ) + len( try2 ) == 0:
            if noRaise:
                return moose.element('/')
            else:
                raise SimError( "findObj: No object found named: '{}'".format( name) )
        if len( try1 ) == 1:
            return try1[0]
        else:
            return try2[0]

    def _scaleParams( self, params ):
        if len(params) == 0:
            return
        if (len(params) % 3) != 0:
            raise SimError( "scaleParam: expecting triplets of [obj, field, scale], got: '{}'".format( params ) )
        for i in range( 0, len(params), 3):
            self._scaleOneParam( params[i:i+3] )

    def _scaleOneParam( self, params ):
        if len(params) != 3:
            raise SimError( "scaleOneParam: expecting [obj, field, scale], got: '{}'".format( params ) )

        obj = self.findObj( '/model', params[0], noRaise = True )
        if obj.path == '/':  # No object found
            return

        scale = float( params[2] )
        if not ( scale >= 0.0 and scale <= 100.0 ):
            print( "Error: Scale {} out of range".format( scale ) )
            assert( False )
        #assert( scale >= 0.0 and scale <= 100.0 )
        if params[1] == 'Kd':
            if not obj.isA[ "ReacBase" ]:
                raise SimError( "scaleParam: can only assign Kd to a Reac, was: '{}'".format( obj.className ) )
            sf = np.sqrt( scale )
            obj.Kb *= sf
            obj.Kf /= sf
        elif params[1] == 'tau':
            obj.Kb /= scale
            obj.Kf /= scale
        else: 
            val = obj.getField( params[1] )
            obj.setField( params[1], val * scale)
        #print("ScaledParam {}.{} from {} to {}".format( params[0], params[1], val, obj.getField( params[1] ) ) )

    def deleteItems( self, kinpath ):
        if self.itemstodelete:
            for ( entity, change ) in self.itemstodelete[:]:
                if entity != "":
                    obj = self.findObj(kinpath, entity)
                    if change == 'delete':
                        if obj.path != kinpath:
                            moose.delete( obj )
                        else:
                            raise SimError("modelId/rootPath is not allowed to delete {}".format( obj) )

    def subsetItems( self, kinpath ):
        nonContainers, directContainers, indirectContainers = [],[],[]
        for i in ['moregraphs', 'info', 'graphs']:
            directContainers.append( moose.element( kinpath + '/' + i ) )
        subsets = re.sub(r'\s', '', self.modelSubset).split(',')

        for i in subsets: 
            elm = self.findObj(kinpath, i)
            if isContainer(elm):
                indirectContainers.extend( getContainerTree(elm, kinpath))
                directContainers.append(elm)
            else:
                indirectContainers.extend( getContainerTree(elm, kinpath))
                nonContainers.append( elm )

        # Eliminate indirectContainers that are descended from a
        # directContainer: all descendants of a direct are included
        dirset = set( [i.path for i in directContainers] )
        indirectContainers = [ i for i in indirectContainers if isNotDescendant( i, dirset ) ]

        # Make the containers unique. Put in a set.
        inset = set( [i.path for i in indirectContainers] )
        nonset = set( [i.path for i in nonContainers] )
        doomed = set()

        # Go through all immediate children of indirectContainers, 
        #   and mark for deletion in doomedList
        for i in inset:
            doomed.update( [j.path for j in moose.wildcardFind( i + '/#[]' ) ] )
        # Remove nonContainers, IndrectContainers and DirectContainers
        #   from doomedList
        doomed = ((doomed - inset) - dirset) - nonset

        # Delete everything in doomedList
        for i in doomed:
            if moose.exists( i ):
                moose.delete( i )
            else:
                print( "Warning: deleting doomed obj {}: it does not exist".format( i ) )

    def modify( self, modelId, erSPlist, odelWarning):
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
        kinpath = modelId.path
        self.deleteItems( kinpath )
        if not( self.modelSubset.lower() == 'all' or self.modelSubset.lower() == 'any' ):
            self.subsetItems( kinpath )

        #Function call for checking dangling Reaction/Enzyme/Function's
        pruneDanglingObj( kinpath, erSPlist)
            
        for (entity, field, value) in self.parameterChange:
            obj = self.findObj(kinpath, entity)
            if field == "concInit (uM)":
                field = "concInit"
            #print " obj ", obj, field, value
            obj.setField( field, value )

            
Model.argNames = ['modelSource', 'citation', 'citationId', 'authors',
            'modelSubset', 'fileName', 'solver', 'notes' ,'scoringFormula','itemstodelete','parameterChange']

##########################################################################
# Utility functions needed by Model class.
                
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

def getObjParam( elm, field ):
    if field == 'Kd':
        if not elm.isA['ReacBase']:
            raise SimError( "getObjParam: can only get Kd on a Reac, was: '{}'".format( obj.className ) )
        return elm.Kb/elm.Kf
    elif field == 'tau':
        # This is a little dubious, because order 1 reac has 1/conc.time
        # units. Suppose Kf = x / mM.sec. Then Kf = 0.001x/uM.sec
        # This latter is the Kf we want to use, assuming typical concs are
        # around 1 uM.
        if not elm.isA['ReacBase']:
            raise SimError( "getObjParam: can only get tau on a Reac, was: '{}'".format( obj.className ) )
        scaleKf = 0.001 ** (elm.numSubstrates-1)
        scaleKb = 0.001 ** (elm.numProducts-1)
        #print( "scaleKf={}; scaleKb={}, numsu ={}, numPrd={},Kb={},Kf={}".format( scaleKf, scaleKb, elm.numSubstrates, elm.numProducts, elm.Kb, elm.Kf ) )
        return 1.0 / ( elm.Kb * scaleKb + elm.Kf * scaleKf )
    else:
        return elm.getField( field )

##########################################################################
class PauseHsolve:
    def __init__(self, optimizeElec = False):
        self.optimizeElec = optimizeElec
        self. epspSettle = 0.5
        self. stimSettle = 2.0


    def setHsolveState(self, state):
        if not self.optimizeElec:
            return
        if moose.exists( '/model/elec/hsolve' ):
            if state:
                for i in range( 9 ):
                    moose.setClock( i, elecDt )
            else:
                for i in range( 9 ):
                    moose.setClock( i, 1e12 )
            moose.setClock( 8, elecPlotDt )

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
            #print "Ret READ DATA from INNERLOAD", len( data )
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

def isContainer( elm ):
    return elm.className == 'Neutral' or elm.isA[ 'ChemCompt']

def pruneDanglingObj( kinpath, erSPlist):
    erlist = moose.wildcardFind(kinpath+"/##[ISA=ReacBase],"+kinpath+ "/##[ISA=EnzBase]")
    subprdNotfound = False
    ratelawchanged = False
    funcIPchanged  = False
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
            elif len(isub) != erSPlist[i]["s"] or len(iprd) != erSPlist[i]["p"]:
                ratelawchanged = True
                mRateLaw = mRateLaw+"\n"+i.path
                
    flist = moose.wildcardFind( kinpath + "/##[ISA=Function]" )
    for i in flist:
        if len(i.neighbors['valueOut']) == 0:
            moose.delete(moose.element(i))
        if len(moose.element(moose.element(i).path+'/x').neighbors['input']) == 0 or  \
            len(moose.element(moose.element(i).path+'/x').neighbors['input']) != i.numVars:
            funcIPchanged = True
            mFunc = mFunc+"\n"+i.path

    if subprdNotfound:
        raise SimError (" \nWarning: Found dangling Reaction/Enzyme, if this/these reac/enz to be deleted then add in the worksheet in ModelMapping -> itemstodelete section. Program will exit for now. "+mWarning)
    if ratelawchanged:
        raise SimError ("\nWarning: This reaction or enzyme's RateLaw needs to be corrected as its substrate or product were deleted while subsetting. Program will exit now. \n"+mRateLaw)
    if funcIPchanged:
        raise SimError ("\nWhile subsetting the either one or more input's to the function is missing, if function need/s to be deleted  then add this/these in the worksheet in ModelMapping -> itemstodelete section or one need to care to bring back those molecule/s, program will exit now.\n"+mFunc)
    

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
            #print( "in putStimsInQ, field = {}".format( i.field ) )
            if i.field in ['Im', 'current', 'Vclamp'] or (i.field=='rate' and 'syn' in i.entities[0]) :
                if val == 0.0:
                    heapq.heappush( q, Qentry(t+pauseHsolve.stimSettle, pauseHsolve, 0) )
                else:
                    heapq.heappush( q, Qentry(t, pauseHsolve, 1) ) # Turn on hsolve

def makeReadoutPlots( readouts, modelLookup ):
    moose.Neutral('/model/plots')
    for i in readouts:
        readoutElms = []
        for j in i.entities:
            readoutElms.extend( modelLookup[j] )
        for elm in readoutElms:
            ######Creating tables for plotting for full run #############
            plotpath = '/model/plots/' + ntpath.basename(elm.name)
            if i.field in elecFields:
                plot = moose.Table(plotpath)
            else:
                plot = moose.Table2(plotpath)
            i.plots[elm.name] = plot
            if i.field in epspFields:   # Do EPSP stuff.
                fieldname = 'getVm'
                i.epspPlot = plot
            elif i.field in epscFields:   # Do EPSC stuff.
                fieldname = 'getCurrent'
                '''
                path = elm.path + '/vclamp'
                if moose.exists( path ):
                    elm = moose.element( path )
                else:
                    raise SimError( "makeReadoutPlots: Cannot find vclamp on {}".format( elm.path ) )
                '''
                i.epspPlot = plot
            else:
                fieldname = 'get' + i.field.title()
            moose.connect( plot, 'requestOut', elm, fieldname )

def putReadoutsInQ( q, readouts, pauseHsolve ):
    stdError  = []
    plotLookup = {}
    for i in readouts:
        if i.field in (epspFields + epscFields):
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

def deliverStim( qe, model ):
    field = qe.entry.field
    #field = model.fieldLookup[s.field]
    for name in qe.entry.entities:
        elms = model.modelLookup[name]
        for e in elms:
            if field == 'Vclamp':
                path = e.path + '/vclamp'
                moose.element( path ).setField( 'command', qe.val )
                #print(" Setting Vclamp {} to {}".format( path, qe.val ))
            else:
                e.setField( field, qe.val )
                #print qe.t, e.path, field, qe.val
                #print( "########Stim = {} {} {} {} {}".format( qe.t, moose.element( '/model/elec/head0/glu' ).modulation, moose.element( '/model/chem/spine/Ca' ).conc, moose.element( '/model/elec/head0/Ca_conc' ).Ca, moose.element( '/model/elec/head0/glu/sh/synapse' ).weight ) )
                if qe.t == 0:
                    ## At time zero we initial the value concInit or nInit
                    if field == 'conc':
                        e.setField("concInit",qe.val)
                        moose.reinit()
                    elif field == "n":
                        e.setField( 'nInit', qe.val )
                        moose.reinit()

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
    ratioReference = 0.0
    if readout.field in (epspFields + epscFields):
        doEpspReadout( readout, model.modelLookup )
    elif val == -1: # This is a special event to get RatioReferenceValue
        doReferenceReadout( readout, model.modelLookup, readout.field )
    else:
        doEntityAndRatioReadout(readout, model.modelLookup, readout.field)

def doEpspReadout( readout, modelLookup ):
    n = int( round( readout.epspWindow / readout.epspPlot.dt ) )
    assert( n > 5 )
    pts = np.array( readout.epspPlot.vector[-n:] )
    #print( "DOING EPSP READOUT WITH " +  readout.field )
    #print( ["{:.3g} ".format( x ) for x in pts] )
    if "slope" in readout.field:
        dpts = pts[1:] - pts[:-1]
        slope = max( abs( dpts ) )/readout.epspPlot.dt
        readout.simData.append( slope )
    elif "peak" in readout.field:
        pts -= pts[0]
        pk = max( abs(pts) )
        readout.simData.append( pk )

def doReferenceReadout( readout, modelLookup, field ):
    ratioReference = 0.0
    assert( readout.ratioReferenceTime >= 0.0 ) # one-time calculation
    for rr in readout.ratioReferenceEntities:
        elms = modelLookup[ rr ]
        for e in elms:
            ratioReference += e.getField( field )
    readout.ratioData.append( ratioReference )

def doEntityAndRatioReadout( readout, modelLookup, field ):
    sim = 0.0
    for rr in readout.entities:
        elms = modelLookup[ rr ]
        for e in elms:
            sim += e.getField( field )
    readout.simData.append( sim )
    ratioReference = 0.0
    if readout.ratioReferenceTime < 0.0 :
        for rr in readout.ratioReferenceEntities:
            elms = modelLookup[ rr ]
            for e in elms:
                ratioReference += e.getField( field )
        readout.ratioData.append( ratioReference )

def doSynInputReadout( readout, modelLookup, field ):
    readout.simData.append( 0 )

def processReadouts( readouts, scoringFormula ):
    numScore  = 0
    score = 0.0
    for i in readouts:
        i.applyRatio()
        score += i.doScore( scoringFormula )
        numScore += 1
    return score/numScore


##########################################################################
def parseAndRun( model, stims, readouts, modelId ):
    q = []
    clock = moose.element( '/clock' )
    putStimsInQ( q, stims, model.pauseHsolve )
    putReadoutsInQ( q, readouts, model.pauseHsolve )

    moose.reinit()
    #model.pauseHsolve.setHsolveState( 0 )
    for i in range( len( q ) ):
        qe = heapq.heappop( q )
        currt = clock.currentTime
        if ( qe.t > currt ):
            moose.start( qe.t - currt )
        if isinstance( qe.entry, Stimulus ):
            deliverStim( qe, model )
        elif isinstance( qe.entry, Readout ):
            doReadout( qe, model )
        elif isinstance( qe.entry, PauseHsolve ):
            qe.entry.setHsolveState( int(qe.val) )

    score = processReadouts( readouts, model.scoringFormula )

    return score


##########################################################################
def parseAndRunDoser( model, stims, readouts, modelId ):
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
    doseMol = model.modelLookup[ stims[0].entities[0]]
    runDoser( model, stims[0], readouts[0], doseMol[0] )
    score = processReadouts( readouts, model.scoringFormula )
    return score
        
##########################################################################
def runDoser( model, stim, readout, doseMol ):
    responseScale = readout.quantityScale
    doseScale = stim.quantityScale
    referenceDose = readout.ratioReferenceDose * stim.quantityScale
    sim = 0.0
    for dose, response, sem in readout.data:
        doseMol.concInit = dose * doseScale
        moose.reinit()
        moose.start( readout.settleTime )
        doEntityAndRatioReadout( readout, model.modelLookup,readout.field )
    if readout.ratioReferenceTime >= 0.0:   # Do a one-time reference.
        doseMol.concInit = referenceDose # Reference conc is first dose.
        moose.reinit()
        if readout.ratioReferenceTime > 0.0: # Get reference at settleTime.
            moose.start( readout.settleTime )
        doReferenceReadout( readout, model.modelLookup,readout.field )

##########################################################################
def setFieldIncludingInit( obj, field, val ):
    obj.setField( field, val )
    if field == 'conc' or field == 'n':
        field2 = field + 'Init'
        obj.setField( field2, val )

def doBarChartStim( multiStimLine, doseMol, dose, field ):
    indices = []
    for i in range( len( multiStimLine ) ):
        if multiStimLine[i] == '1' or multiStimLine[i] == '+':
            indices.append(i)
    for j in indices:
        setFieldIncludingInit( doseMol[j], field, dose[j] )

def doBarChartReference( readout, stim, modelLookup ):
    if readout.useRatio and readout.ratioReferenceTime >= 0.0:
        responseScale = readout.quantityScale
        referenceDose = readout.ratioReferenceDose * stim.quantityScale
        referenceMol = modelLookup[readout.ratioReferenceEntities[0] ]

        setFieldIncludingInit( referenceMol[0], readout.field, referenceDose )
        moose.reinit()
        if readout.ratioReferenceTime > 0.0: # Get reference at settleTime.
            moose.start( readout.settleTime )
        doReferenceReadout( readout, modelLookup,readout.field )

def doBarChartBars( readout, stim, modelLookup ):
    doseMol, dose, origDose = setUpBarChartStims( stim, modelLookup )
    for i in readout.data:
        doBarChartStim( i[0], doseMol, dose, stim.field )
        moose.reinit()
        moose.start( readout.settleTime )
        doEntityAndRatioReadout(readout, modelLookup, readout.field)
        for mol, val in zip( doseMol, origDose ):
            setFieldIncludingInit( mol, stim.field, val )
    return doseMol, origDose

def setUpBarChartStims( stim, modelLookup ):
    doseMol = []
    dose = []
    origDose = []
    #Stimulus Molecules
    #Assuming one stimulus block, one molecule allowed
    for i in stim.data:
        if not i[0] in modelLookup:
            raise SimError( "parseAndRunBarChart: stimulus entity '{}' not mapped to model entities".format( i[0] ) )
        obj = modelLookup[ i[0] ][0]
        doseMol.append( obj )
        dose.append( i[1] * stim.quantityScale )
        origDose.append( obj.getField( stim.field ) )
    return doseMol, dose, origDose

def parseAndRunBarChart( model, stims, readouts, modelId ):
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
        print( "Currently unable to handle automatic settling to stead-state in doseResponse, using default 300 s." )
        runTime = 300
    
    doseMol, origDose = doBarChartBars( readouts[0], stims[0], model.modelLookup )

    doBarChartReference( readouts[0], stims[0], model.modelLookup )
    for mol, val in zip( doseMol, origDose ):
        setFieldIncludingInit( mol, stims[0].field, val )

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

def buildSolver( modelId, solver, useVclamp = False ):
    # Here we remove and rebuild the HSolver because we have to add vclamp
    # after loading the model.
    if useVclamp: 
        if moose.exists( '/model/elec/hsolve' ):
            raise SimError( "Hsolve already created. Please rebuild model without HSolve. In rdesigneur use the 'turnOffElec = True' flag." )
    if moose.exists( '/model/elec/soma' ) and not moose.exists( '/model/elec/hsolve' ):
        for i in range( 9 ):
            moose.setClock( i, elecDt )
        moose.setClock( 8, elecPlotDt )
        tgt = '/model/elec/soma'
        hsolve = moose.HSolve( '/model/elec/hsolve' )
        hsolve.dt = elecDt
        hsolve.target = tgt
        moose.reinit()

    compts = moose.wildcardFind( modelId.path + '/##[ISA=ChemCompt]' )
    for compt in compts:
        if solver.lower() in ['none','ee','exponential euler method (ee)']:
            return
        if len( moose.wildcardFind( compt.path + "/##[ISA=Stoich]" ) ) > 0:
            print( "findSim::buildSolver: Warning: Solvers already defined. Use 'none' or 'ee' in solver specifier" )
            return
        if solver.lower() in ['gssa','stochastic simulation (gssa)']:
            ksolve = moose.Gsolve ( compt.path + '/gsolve' )
        elif solver.lower() in ['gsl','runge kutta method (gsl)']:
            ksolve = moose.Ksolve( compt.path + '/ksolve' )
        stoich = moose.Stoich( compt.path + '/stoich' )
        stoich.compartment = moose.element( compt.path )
        stoich.ksolve = ksolve
        #print( "Path = " + compt.path + "/##" )
        stoich.path = compt.path + '/##'

def buildVclamp( stim, modelLookup ):
    # Stim.entities should be the compartment name here.
    compt = modelLookup[stim.entities[0]][0]
    path = compt.path
    vclamp = moose.VClamp( path + '/vclamp' )
    modelLookup['vclamp'] = [vclamp,]
    vclamp.mode = 0     # Default. could try 1, 2 as well
    vclamp.tau = 0.2e-3 # lowpass filter for command voltage input
    vclamp.ti = 20e-6   # Integral time
    vclamp.td = 5e-6    # Differential time. Should it be >= dt?
    #vclamp.gain = 0.00005   # Gain of vclamp ckt used for squid: 500x500um
    vclamp.gain = compt.Cm * 5e3  # assume SI units. Scaled by area so that gain is reasonable. Needed to avert NaNs.
    #print( "Building Vclamp on {}. Compt Cm = {}".format( path, compt.Cm ))

    # Connect voltage clamp circuitry
    moose.connect( compt, 'VmOut', vclamp, 'sensedIn' )
    moose.connect( vclamp, 'currentOut', compt, 'injectMsg' )
    moose.reinit()

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
    print ("Concinit = {}".format( obj.concInit ) )
    raise SimError( "getUniqueName: {} and {} non-unique, please rename.".format( wf[0].path, wf[1].path ) )
    return obj.name


def generateParamFile( model, fname ):
    with open( fname, "w" ) as fp:
        for i in moose.wildcardFind( model + "/##[ISA=PoolBase]" ):
            conc = i.concInit
            if conc > 0.0:
                objName = getUniqueName( model, i )
                fp.write( "{}   concInit\n".format( objName ) )

        for i in moose.wildcardFind( model + "/##[ISA=ReacBase]" ):
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

def runit( expt, model, stims, readouts, modelId ):
    for i in stims:
        i.configure( model.modelLookup )
    for i in readouts:
        i.configure( model.modelLookup )

    if "doseresponse" in expt.exptType:
        return parseAndRunDoser( model, stims, readouts, modelId)
    elif "timeseries" in expt.exptType:
        return parseAndRun( model, stims, readouts, modelId )
    elif "barchart" in expt.exptType:
        return parseAndRunBarChart( model, stims, readouts, modelId )
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
    parser.add_argument( '-hp', '--hide_plot', action="store_true", help='Hide plot output of simulation along with expected values. Default is to show plot.' )
    parser.add_argument( '-hs', '--hide_subplots', action="store_true", help='Hide subplot output of simulation. By default the graphs include dotted lines to indicate individual quantities (e.g., states of a molecule) that are being summed to give a total response. This flag turns off just those dotted lines, while leaving the main plot intact.' )
    parser.add_argument( '-o', '--optimize_elec', action="store_true", help='Optimize electrical computation. By default the electrical computation runs for the entire duration of the simulation. With this flag the system turns off the electrical engine except during the times when electrical stimuli are being given. This can be *much* faster.' )
    parser.add_argument( '-s', '--scale_param', nargs=3, default=[],  help='Scale specified object.field by ratio.' )
    parser.add_argument( '-settle_time', '--settle_time', type=float, default=0,  help='Run model for specified settle time and return dict of {path,conc}.' )
    args = parser.parse_args()
    innerMain( args.script, modelFile = args.model, dumpFname = args.dump_subset, paramFname = args.param_file, hidePlot = args.hide_plot, hideSubplots = args.hide_subplots, optimizeElec = args.optimize_elec, scaleParam = args.scale_param, settleTime = args.settle_time )


def innerMain( script, modelFile = "model/synSynth7.g", dumpFname = "", paramFname = "", hidePlot = True, hideSubplots = False, optimizeElec=True, silent = False, scaleParam=[], settleTime = 0, settleDict = {} ):
    ''' If *settleTime* > 0, then we need to return a dict of concs of
    all variable pools in the chem model obtained after loading in model, 
    applying all modifications, and running for specified settle time.\n
    If the *settleDict* is not empty, then the system goes through and 
    matches up pools to assign initial concentrations.
    '''

    global pause
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    modelWarning = ""
    modelId = ""
    expt, stims, readouts, model = loadTsv( script )
    if modelFile != "":
        model.fileName = modelFile
    model.pauseHsolve = PauseHsolve( optimizeElec )
    #This list holds the entire models Reac/Enz sub/prd list for reference
    erSPlist = {}
    # First we load in the model using EE so it is easier to tweak
    try:
        if not os.path.isfile(model.fileName):
            raise SimError( "Model file name {} not found".format( model.fileName ) )
        fileName, file_extension = os.path.splitext(model.fileName)
        if file_extension == '.xml':
            modelId, errormsg = moose.mooseReadSBML( model.fileName, 'model', 'ee' )
        elif file_extension == '.g':
            modelId = moose.loadModel( model.fileName, 'model', 'ee' )
        # moose.delete('/model[0]/kinetics[0]/compartment_1[0]')
        elif file_extension == '.py':
            # Assume a moose script for creating the model. It must have a
            # function load() which returns the id of the object containing
            # the model. At this point the model must be in the current dir
            mscript = imp.load_source( "mscript", model.fileName )
            #mscript = __import__( fileName )
            modelId = mscript.load()


        for f in moose.wildcardFind('/model/##[ISA=ReacBase],/model/##[ISA=EnzBase]'):
            erSPlist[f] = {'s':len(f.neighbors['sub']), 'p':len(f.neighbors['prd'])}
        # Then we apply whatever modifications are specified by user or protocol

        modelWarning = ""
        model.modify( modelId, erSPlist,modelWarning )
        model._scaleParams( scaleParam )
        if len(dumpFname) > 2:
            if dumpFname[-2:] == '.g':
                moose.mooseWriteKkit( modelId.path, dumpFname )
            elif len(dumpFname) > 4 and dumpFname[-4:] == '.xml':
                moose.mooseWriteSBML( modelId.path, dumpFname )
            else:
                raise SimError( "Subset file type not known for '{}'".format( dumpFname ) )

        if len(paramFname) > 0:
            generateParamFile( modelId.path, paramFname )
            quit()


        model.buildModelLookup()


        if expt.exptType == 'directparameter':
            score = Readout.directParamScore( readouts, model.modelLookup, model.scoringFormula )
            if not hidePlot:
                print( "Score = {:.3f} for\t{}\tElapsed Time = 0.0 s".format( score, os.path.basename(script) ) )
            moose.delete( modelId )
            if moose.exists( '/library' ):
                moose.delete( '/library' )
            return score

        '''
        for i in stims:
            if i.field == 'Vclamp':
                buildVclamp( i, model.modelLookup )
        '''

        
        '''
        if stims[0].field == 'Vclamp':
            readouts[0].entities = ['vclamp']
            #readouts[0].field = 'current'
            buildVclamp( stims[0], model.modelLookup )
        '''


        hasVclamp = False
        readoutStim = stims[0]
        for i in stims:
            if i.field.lower() == 'vclamp':
                hasVclamp = True
                buildVclamp( i, model.modelLookup )
            elif i.field.lower() == 'inject':
                readoutStim = i
            if len(i.entities) > 0 and i.entities[0].lower() == 'syninput':
                readoutStim = i
        if readouts[0].field in ( epspFields + epscFields ):
            readouts[0].stim = readoutStim 
        makeReadoutPlots( readouts, model.modelLookup )
        if hasVclamp:
            #build the solver with a flag to say rebuild the hsolve.
            buildSolver( modelId, model.solver, useVclamp = True )
        else:
            buildSolver( modelId, model.solver )
        if file_extension != '.py': # rdesigneur sims will set own clocks
            for i in range( 10, 20 ):
                moose.setClock( i, 0.1 )

        ##############################################################
        # Here we handle presettling. First to generate, then to apply
        # the dict of settled values.
        if settleTime > 0:
            t0 = time.time()
            moose.reinit()
            #print settleTime
            moose.start( settleTime )
            w = moose.wildcardFind( modelId.path + "/##[ISA=PoolBase]" )
            ret = {}
            for i in w:
                if not i.isBuffered:
                    ret[i.path] = i.n
                    #print( "{}.nInit =   {:.3f}".format( i.path, i.n ))
            #print "-------------------- settle done -------------------"
            moose.delete( modelId )
            if moose.exists( '/library' ):
                moose.delete( '/library' )
            #print( "Done settling in {:.2f} seconds".format( time.time()-t0))
            print( "s", end = '' )
            sys.stdout.flush()
            return ret

        for key, value in settleDict.items():
            moose.element( key ).nInit = value
        ##############################################################

        t0 = time.time()
        score = runit( expt, model,stims, readouts, modelId )
        elapsedTime = time.time() - t0
        if not hidePlot:
            print( "Score = {:.3f} for\t{}\tElapsed Time = {:.1f} s".format( score, os.path.basename(script), elapsedTime ) )
            for i in readouts:
                pylab.figure(1)
                i.displayPlots( script, model.modelLookup, stims[0], hideSubplots, expt.exptType )
                
            pylab.show()
        moose.delete( modelId )
        if moose.exists( '/library' ):
            moose.delete( '/library' )
        return score
        
    except SimError as msg:
        if not silent:
            print( "Error: findSim failed for script {}: {}".format(script, msg ))
        if modelId:
            moose.delete( modelId )
            if moose.exists( '/library' ):
                moose.delete( '/library' )
        return -1.0
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
