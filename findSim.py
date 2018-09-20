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

import heapq
import pylab
import numpy
import sys
import argparse
import moose
import os
import re
import ntpath
convertTimeUnits = {('sec','s') : 1.0, 
    ('ms','millisec', 'msec') : 1e-3,('us','microsec') : 1e-6, 
    ('ns','nanosec') : 1e-9, ('min','m') : 60.0, 
    ('hours','hrs') : 3600.0, "days": 86400.0}
#convertConcUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 'nM':1.0e-6, 'pM': 1.0e-9, 'number':1.0, 'ratio':1.0 }
#convertVoltageUnits = { 'V': 1, 'mV': 0.001, 'uV': 1.0e-6, 'nV':1.0e-9 }
#convertCurrentUnits = { 'A': 1, 'mA': 0.001, 'uA': 1.0e-6, 'nA':1.0e-9, 'pA':1.0e-12 }
convertQuantityUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 
        'nM':1.0e-6, 'pM': 1.0e-9, 'number':1.0, 'ratio':1.0, 
        'V': 1, 'mV': 0.001, 'uV': 1.0e-6, 'nV':1.0e-9,
        'A': 1, 'mA': 0.001, 'uA': 1.0e-6, 'nA':1.0e-9, 'pA':1.0e-12 }

#elecFields = ['V', 'mV', 'uV', 'nV', 'A', 'mA', 'uA', 'nA', 'pA' ]
elecFields = ['Vm', 'Im']


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
            if doneContext and (len( cols ) == 0 or cols[0] == '' or cols[0].isspace()):
                break
            if cols[0] == "Experiment context":
                doneContext = True
                continue
            for i in Experiment.argNames:
                if keywordMatches( cols[0], i ):
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
            raise SimError(" Stimulus::__init__: quantity units not known.")
        temp = entities.split( ',' )
        self.entities = [ i for i in temp if len(i) > 0 ]
        """Name of the model entity to modify for the stimulus. 
        Typically a molecule name, or a compartment in a neuron."""
        self.field = field
        """Name of the field associated with the entity. For example,
        conc for a molecule, or currentInjection for compartment"""
        self.data = data
        """List of pairs of numbers for stimulus, Each row is [time or dose, quantity]"""

    def __lt__( self, other ):
        return self.data < other.data

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
            field = '',
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
            raise SimError( "Readout::__init__: unknown quantity units" +
                    self.quantityUnits )

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

    def __lt__( self, other ):
        return self.data < other.data
        
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
                    pp.plotme( fname, joinSimPoints = True )
        elif "timeseries" in exptType:
            for i in self.entities:
                elms = modelLookup[i]
                ypts = self.plots[elms[0].name].vector
                numPts = len( ypts )
                if numPts > 0:
                    tconv = next( v for k, v in convertTimeUnits.items() if self.timeUnits in k )
                    xpts = numpy.array( range( numPts)  ) * self.plots[elms[0].name].dt / tconv
                sumvec = numpy.zeros(len(xpts))
                for j in elms:
                    #pp = PlotPanel( self, xlabel = j.name +'('+self.timeUnits+')' )
                    pp = PlotPanel( self, exptType )
                # Here we plot the fine timeseries for the sim.
                # Not yet working for all options of ratio.
                    if len( self.ratioData ) > 0:
                        scale = self.quantityScale * self.ratioData[0]
                    else:
                        scale = self.quantityScale
                    if self.useNormalization and abs(self._simDataReference) > 1e-15:
                        scale *= self._simDataReference/self.quantityScale
                    ypts = self.plots[j.name].vector / scale
                    sumvec += ypts
                    if (not hideSubplots) and len( elms ) > 1: 
                        # Plot summed components
                        pylab.plot( xpts, ypts, 'r:', label = j.name )

                pylab.plot( xpts, sumvec, 'r--' )
                pp.plotme( fname )

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
            normalization = self.simData[0] / rd[0]
            self._simDataReference = normalization
        else:
            normalization = self.quantityScale
        
        self.simData = [ s/(r * normalization) for s, r in zip( self.simData, rd ) ]

    def doScore( self, scoringFormula ):
        assert( len(self.data) == len( self.simData ) )
        score = 0.0
        numScore = 1.0
        for i,sim in zip( self.data, self.simData ):
            t = i[0]
            expt = i[1]
            sem = i[2]
            #print i
            #print t, expt, sem, sim
            #print "Formula = ", scoringFormula, eval( scoringFormula )
            score += eval( scoringFormula )
            numScore += 1.0

        return score/numScore


    def load( fd ):
        arg, data, param, struct, modelLookup = innerLoad( fd, Readout.argNames, dataWidth = 3 )
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
        #print "################ Loading model, lookup=", modelLookup
        # model.modelLookup = {} from constructor.
        model._tempModelLookup = modelLookup
        #model.fieldLookup = fieldLookup
        return model

    load = staticmethod( load )

    def buildModelLookup( self ):
        for i in self._tempModelLookup:
            paths = self._tempModelLookup[i].split('+')
            # Summed sim entities are separated with a '+', but map to a 
            # single experimentally defined entity.
            foundObj = [ self.findObj( '/model', p) for p in paths ]
            self.modelLookup[i] = foundObj
    '''
    def buildFieldLookup( self, stims, readouts ):
        for i in stims:
            if not i.field in self.fieldLookup:
                self.fieldLookup[i.field] = i.field
        for i in readouts:
            if not i.field in self.fieldLookup:
                self.fieldLookup[i.field] = i.field
    '''

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
        # if change == 'delete':
        #     self.StructuralChange.append( ( entity, change ) )
        # else:
        #     print( "Warning: Model::addStructuralChange: Unknown modification: " + change )
    def findObj( self,rootpath, name ):
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
        #print " findObj ",rootpath+'/'+name, moose.wildcardFind(rootpath+'/'+name)
        #print " findObj 2",rootpath+'/##/'+name, moose.wildcardFind(rootpath+'/##/'+name)
        if len( try1 ) + len( try2 ) > 1:
            raise SimError( "findObj: ambiguous name: '{}'".format(name) )
        if len( try1 ) + len( try2 ) == 0:
            raise SimError( "findObj: No object found on: '{}'".format( name) )
        if len( try1 ) == 1:
            return try1[0]
        else:
            return try2[0]

    def modify( self, modelId, erSPlist, odelWarning):
        # Start off with things explicitly specified for deletion.
        kinpath = modelId.path
        if self.itemstodelete:
            for ( entity, change ) in self.itemstodelete[:]:
                if entity != "":
                    obj = self.findObj(kinpath, entity)
                    if change == 'delete':
                        if obj.path != modelId.path and obj.path != '/model[0]':
                            moose.delete( obj )
                        else:
                            raise SimError("modelId/rootPath is not allowed to delete {}".format( obj) )
                
        if not( self.modelSubset.lower() == 'all' or self.modelSubset.lower() == 'any' ):
            '''If group and group/obj is written in model subset, then entire group is saved and nothing \ 
                specific is delete from the group.
                And if group/obj is written then group's obj is saved.
            '''
            # Generate list of all included groups
            allCompts, directCompts, indirectCompts = [], [], []
            allGroups, directGroups, indirectGroups = [], [], []
            
            #Get all Groups under all compartment, all compartment under model
            for c in moose.wildcardFind(kinpath+'/##[ISA=ChemCompt]'):
                allCompts.append(c)
                for grps in moose.wildcardFind(c.path+'/##[TYPE=Neutral]'):
                    allGroups.append(grps)

            subsets = re.sub(r'\s', '', self.modelSubset).split(',')
            nonGroups = []
            nonCompts = []
            survivorsGroup = []
            #here all the object direct and indirect groups and compartment is queried
            #indirectgroup/compartment are those in which group/object or comparetment/object
            #are specified in modelmapping

            for i in subsets: 
                elm = self.findObj(kinpath, i)
                if isCompartment(elm):
                    directCompts.append(elm)
                elif isGroup( elm ):
                    directGroups.extend( findChildGroups( elm ) )
                    survivorsGroup.append(elm)
                    objCompt = findCompartment(elm)
                    if (moose.element(objCompt).className in ["CubeMesh","CyclMesh"]):
                        indirectCompts.append(objCompt)
                else:
                    obj = findParentGroup(elm)
                    if (moose.element(obj).className == "Neutral"):
                        indirectGroups.append( obj )
                        nonGroups.append(elm)
                        objCompt = findCompartment(obj)
                        if (moose.element(objCompt).className in ["CubeMesh","CyclMesh"]):
                            indirectCompts.append(objCompt)
                    elif (moose.element(obj).className in ["CubeMesh","CyclMesh"]):
                        indirectCompts.append(obj)
                        nonCompts.append(elm)
            
            includedGroups = set( directGroups + indirectGroups )
            allGroups = set(allGroups)
            # Find groups to delete, and delete them.
            excludedGroups = allGroups - includedGroups
            for i in excludedGroups:
                moose.delete( i )

            # Generate list of all surviving objects. We're going to get
            # rid of them too, unless they are saved by the subset list.
            survivors = []
            for c in moose.wildcardFind(kinpath+'/##[ISA=ChemCompt]'):
                for grps in moose.wildcardFind(c.path+'/##[TYPE=Neutral]'):
                    survivors.append(grps)
            survivors = set(survivors)
            # Go through the subsets again in case some are already deleted
            nonGroupSet = ornamentPools( nonGroups )
            nonComptSet = ornamentPools( nonCompts )

            for l in survivors-set(survivorsGroup):
                elmGrp = set(moose.wildcardFind(l.path+'/##[ISA=PoolBase]'+','+ l.path+'/##[ISA=ReacBase]'))
                deleteObjsfromGroup = list(elmGrp-nonGroupSet)
                deleteObjsfromGroup = [i for i in deleteObjsfromGroup if not isinstance(moose.element(i.parent), moose.EnzBase)]
                for elmGrpl in deleteObjsfromGroup:
                    if moose.exists(elmGrpl.path):
                         moose.delete(elmGrpl)
            #getting rid of object which are not specified under compartment
            for l in set(allCompts)-set(directCompts):
                elmCmpt = set(moose.wildcardFind(l.path+'/#[ISA=PoolBase]'+','+ l.path+'/#[ISA=ReacBase]'))
                deleteObjsfromCompt = list(elmCmpt-nonComptSet)
                deleteObjsfromCompt = [i for i in deleteObjsfromCompt if not isinstance(moose.element(i.parent), moose.EnzBase)]
                for elmCmpt in deleteObjsfromCompt:
                    if moose.exists(elmCmpt.path):
                         moose.delete(elmCmpt)
            #deleting compartment 
            for dc in set(set(allCompts) - set(directCompts+indirectCompts)):
                moose.delete(dc)
            
            for (entity, field, value) in self.parameterChange:
                obj = self.findObj(kinpath, entity)
                if field == "concInit (uM)":
                    field = "concInit"
                #print " obj ", obj, field, value
                obj.setField( field, value )

            #Function call for checking dangling Reaction/Enzyme/Function's
            pruneDanglingObj( kinpath, erSPlist)
            
Model.argNames = ['modelSource', 'citation', 'citationId', 'authors',
            'modelSubset', 'fileName', 'solver', 'notes' ,'scoringFormula','itemstodelete','parameterChange']

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

        if keywordMatches( cols[0], 'modelLookup' ):
            # Lines of the form exptName1:simName1,exptName2:simName2,...
            if cols[1] != "":
                temp = cols[1].split( ',' )
                modelLookup = { i.split(':')[0]:i.split(':')[1] for i in temp }
        '''
        if keywordMatches( cols[0], 'fieldLookup' ):
            # Lines of the form exptName1:simName1,exptName2:simName2,...
            if cols[1] != "":
                temp = cols[1].split( ',' )
                fieldLookup = { i.split(':')[0]:i.split(':')[1] for i in temp }
        '''

        if keywordMatches( cols[0], 'Data' ):
            readData( fd, data, dataWidth )
            #print "Ret READ DATA from INNERLOAD", len( data )
            return arg, data, param, struct, modelLookup

        for i in argNames:
            if keywordMatches( cols[0], i ):
                arg[i] = str.strip( nonBlank( cols) )
                continue
        if keywordMatches(cols[0],"parameterChange"):
            readParameter(fd,param,dataWidth)

        if keywordMatches( cols[0], 'itemstodelete' ):
            struct= cols[1].split(',')

    return arg, data, param, struct, modelLookup

def nonBlank( cols ):
    for i in cols[1:]:
        if i != '':
            return i
    return ''

def readData( fd, data, width ):
    entityNameInFirstRow = False
    for line in fd:
        cols = line.split("\t" )
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            break
        cl = cols[0].lower()
        if cl == "time" or cl == "dose" or cl == "settletime" or cl == 'entity':
            if cl == 'entity':
                entityNameInFirstRow = True
            continue
        row = []
        for i in range( len( cols ) ):
            if cols[i] != '':
                if i == 0 and entityNameInFirstRow:
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
        if cols[0].lower() == "object":
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

def isGroup( elm ):
    return elm.className == 'Neutral' or elm.className.find( 'Mesh' ) != -1

def isCompartment( elm ):
    return elm.className in ['CubeMesh','CyclMesh'] or elm.className.find( 'Mesh' ) != -1

def findChildGroups( elm ):
    return list( (elm,) + moose.wildcardFind( elm.path + '/##[TYPE=Neutral],' + elm.path + '/##[ISA=ChemCompt]' ) )

def findCompartment(element):
    if element.path == '/':
        return moose.element('/')
    elif mooseIsInstance(element, ["CubeMesh", "CyclMesh"]):
        return (element)
    else:
        return findCompartment(moose.element(element.parent))

def mooseIsInstance(element, classNames):
    return moose.element(element).__class__.__name__ in classNames

def findParentGroup( elm ):
    
    if isGroup( elm ):
        return elm
    if elm.parent.name == 'root':
        print( 'Warning: findParentGroup: root element found, likely naming error' )
        #return moose.element( '/model/kinetics' )
        return moose.element('/model')
    return findParentGroup( elm.parent )

def pruneExcludedElements( elms ):
    #Eliminate all elments in list whose parents are also in list.
    prunes = set( [ i for i in elms if i.parent in elms ] )
    return elms - prunes

def ornamentPools( elms ):
    #Add to the list all descendants of pools: enzymes, cplx, funcs...
    # Do things uniquely and avoiding indices
    s1 = set( elms )
    appendees = []
    for i in s1:
        if i.className.find( 'Pool' ) != -1:
            appendees.extend( i.children )
            for j in set( i.children ):
                appendees.extend( j[0].children )

    ret = set( elms + [k[0] for k in appendees] )
    return ret
    #elms.extend( list(set(appendees)) ) # make it unique.
    
def pruneDanglingObj( kinpath, erSPlist):
    erlist = moose.wildcardFind(kinpath+"/##[ISA=ReacBase],"+kinpath+ "/##[ISA=EnzBase]")
    subprdNotfound = False
    ratelawchanged = False
    funcIPchanged  = False
    mWarning = ""
    mRateLaw = ""
    mFunc = ""
    #modelWarning = ""
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
def putStimsInQ( q, stims, modelLookup ):
    for i in stims:
        for j in i.data:
            if len(j) == 0:
                continue
            elif len(j) == 1:
                val = 0.0
            else:
                val = float(j[1]) * i.quantityScale
            heapq.heappush( q, (float(j[0])*i.timeScale, [i, val ] ) )

def makeReadoutPlots( readouts, modelLookup ):
    moose.Neutral('/model/plots')
    for i in readouts:
        readoutElms = []
        for j in i.entities:
            #print j, modelLookup[j]
            readoutElms.extend( modelLookup[j] )
        #readoutElms = [ moose.element( modelLookup[j][0] ) for j in i.entities ]
        for elm in readoutElms:
            ######Creating tables for plotting for full run #############
            plotpath = '/model/plots/' + ntpath.basename(elm.name)
            if i.field in elecFields:
                plot = moose.Table(plotpath)
            else:
                plot = moose.Table2(plotpath)
            i.plots[elm.name] = plot
            fieldname = 'get' + i.field.title()
            moose.connect( plot, 'requestOut', elm, fieldname )

        #################### temp stuff for debugging #################

        #plot = moose.Table( '/model/plots/Vm' )
        #moose.connect( '/model/plots/Vm', 'requestOut', '/model/elec/soma',  'getVm' )
        #plot = moose.Table( '/model/plots/Vhold' )
        #moose.connect( '/model/plots/Vhold', 'requestOut', '/model/elec/soma/lowpass',  'getInject' )
        #plot = moose.Table( '/model/plots/vclampCurr' )
        #moose.connect( '/model/plots/vclampCurr', 'requestOut', '/model/elec/soma/pid',  'outputValue' )
        #################### temp stuff for debugging #################

def putReadoutsInQ( q, readouts, modelLookup ):
    stdError  = []
    plotLookup = {}
    for i in readouts:
        for j in range( len( i.data ) ):
            # We push in the index of the data entry so the readout can
            # process it when it is run. It will grab both the readout and
            # ratio reference if needed.
            heapq.heappush( q, (float(i.data[j][0])*i.timeScale, [i, j] ) )

        if i.useRatio and i.ratioReferenceTime >= 0.0:
            # We push in -1 to signify that this is to get ratio reference
            heapq.heappush( q, (float(i.ratioReferenceTime)*i.timeScale, [i, -1] ) )

def deliverStim( t, event, model ):
    s = event[0]
    val = event[1]
    #field = model.fieldLookup[s.field]
    for name in s.entities:
        elms = model.modelLookup[name]
        for e in elms:
            if s.field == 'Vclamp':
                path = e.path + '/lowpass'
                moose.element( path ).setField( 'inject', val )
                #moose.showfield( '/model/elec/soma/pid', 'sensed' )
            else:
                e.setField( s.field, val )
                if t == 0:
                    ##At time zero we initial the value concInit or nInit
                    if s.field == 'conc':
                        e.setField("concInit",val)
                        moose.reinit()
                    elif s.field == "n":
                        e.setField( 'nInit', val )
                        moose.reinit()

def doReadout( t, event, model ):
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
    readout = event[0]
    val = int(round( ( event[1] ) ) )
    ratioReference = 0.0
    #field = model.fieldLookup[readout.field]
    if val == -1: # This is a special event to get RatioReferenceValue
        doReferenceReadout( readout, model.modelLookup, readout.field )
    else:
        doEntityAndRatioReadout(readout, model.modelLookup, readout.field)

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
    putStimsInQ( q, stims, model.modelLookup )
    putReadoutsInQ( q, readouts, model.modelLookup )

    moose.reinit()
    for i in range( len( q ) ):
        t, event = heapq.heappop( q )
        currt = clock.currentTime
        if ( t > currt ):
            moose.start( t - currt )
        if isinstance( event[0], Stimulus ):
            deliverStim( t, event, model )
        elif isinstance( event[0], Readout ):
            doReadout( t, event, model )

    score = processReadouts( readouts, model.scoringFormula )

    return score


##########################################################################
def parseAndRunDoser( model, stims, readouts, modelId ):
    if len( stims ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs exactly one stimulus block, {} defined".format( len( stims ) ) )
    if len( readouts ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs exactly one readout block, {} defined".format( len( readout ) ) )
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
def doBarChartStim( multiStimLine, doseMol, dose, field ):
    indices = []
    for i in range( len( multiStimLine ) ):
        if multiStimLine[i] == '1' or multiStimLine[i] == '+':
            indices.append(i)
    for j in indices:
        #print "Stimulating index {} for mol{} and field {} with dose {}".format( j, doseMol[j], field, dose[j] )
        doseMol[j][0].setField( field, dose[j] )
        if field == 'conc' or field == 'n':
            field2 = field + 'Init'
        doseMol[j][0].setField( field2, dose[j] )
        
        

def parseAndRunBarChart( model, stims, readouts, modelId ):
    if len( stims ) != 1:
        raise SimError( "parseAndRunBarChart: BarChart run needs exactly one stimulus block, {} defined".format( len( stims ) ) )
    if len( readouts ) != 1:
        raise SimError( "parseAndRunBarChart: BarChart run needs exactly one readout block, {} defined".format( len( readout ) ) )
    numLevels = len( readouts[0].data )
    
    if numLevels == 0:
        raise SimError( "parseAndRunBarChart: no stimulus levels defined for run" )
    
    runTime = readouts[0].settleTime
    
    if runTime <= 0.0:
        print( "Currently unable to handle automatic settling to stead-state in doseResponse, using default 300 s." )
        runTime = 300
    
    doseMol = []
    dose = []
    #Stimulus Molecules
    #Assuming one stimulus block, one molecule allowed
    for i in stims[0].data:
        doseMol.append( model.modelLookup[ i[0] ] )
        dose.append( i[1] )
    for i in readouts[0].data:
        doBarChartStim( i[0], doseMol, dose, stims[0].field )
        moose.reinit()
        moose.start( readouts[0].settleTime )
        doEntityAndRatioReadout(readouts[0], model.modelLookup, readouts[0].field)

    score = processReadouts( readouts, model.scoringFormula )
    return score

##########################################################################

class PlotPanel:
    def __init__( self, readout, exptType, xlabel = '' ):
        self.name=[]
        for i in readout.entities:
            self.name.append( i )
            #print "Readout Entities:", i
        self.exptType = exptType
        self.useXlog = readout.useXlog
        self.useYlog = readout.useYlog
        if len( xlabel ) > 0:
            self.xlabel = xlabel
        else:
            self.xlabel = 'Time ({})'.format( readout.timeUnits )

        self.xpts = [ i[0] for i in readout.data]
        self.sim = readout.simData # handle ratios...
        self.expt = [ i[1] for i in readout.data]
        self.yerror = [ i[2] for i in readout.data]
        self.sumName=""
        for i in self.name:
            self.sumName += i
            self.sumName += " "
            self.ylabel = i+' ({})'.format( readout.quantityUnits ) #problem here.check so that y-axis are for diff plts not in one plot

    def plotme( self, scriptName, joinSimPoints = False ):
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
        pylab.ylabel( self.ylabel )
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
                    if cols[0] == 'Experiment metadata':
                        expt = Experiment.load(fd )
                    if cols[0] == 'Stimuli':
                        stims.append( Stimulus.load(fd ) )
                    if cols[0] == 'Readouts':
                        readouts.append( Readout.load(fd) )
                    if cols[0] == 'Model mapping':
                        model = Model.load(fd )
    return expt, stims, readouts, model

def buildSolver( modelId, solver, useVclamp = False ):
    compts = moose.wildcardFind( modelId.path + '/##[ISA=ChemCompt]' )
    for compt in compts:
        if solver.lower() in ['ee', 'exponential euler method (ee)']:
            return
        if solver.lower() in ['gssa','stochastic simulation (gssa)']:
            ksolve = moose.Gsolve ( compt.path + '/gsolve' )
        elif solver.lower() in ['gsl','runge kutta method (gsl)']:
            ksolve = moose.Ksolve( compt.path + '/ksolve' )
        stoich = moose.Stoich( compt.path + '/stoich' )
        stoich.compartment = moose.element( compt.path )
        stoich.ksolve = ksolve
        stoich.path = compt.path + '/##'
    # Here we remove and rebuild the HSolver because we have to add vclamp
    # after loading the model.
    if useVclamp and moose.exists( '/model/elec/hsolve' ):
        origHsolve = moose.element( '/model/elec/hsolve' )
        dt = origHsolve.dt
        tgt = origHsolve.target
        moose.delete( '/model/elec/hsolve' )
        moose.reinit()
        hsolve = moose.HSolve( '/model/elec/hsolve' )
        hsolve.dt = dt
        hsolve.target = tgt
        moose.reinit()


def buildVclamp( stim, modelLookup ):
    # Stim.entities should be the compartment name here.
    compt = modelLookup[stim.entities[0]][0]
    path = compt.path
    lowpass = moose.RC(path+"/lowpass") # lowpass filter
    lowpass.R = 50000             # 500 ohms
    lowpass.C = 0.01e-6          # 0.1 uF
    lowpass.V0 = compt.initVm
    print( lowpass.C, compt.Cm, compt.Rm, compt.initVm )
    lowpass.inject = -0.065
    vclamp = moose.DiffAmp(path+"/vclamp")
    vclamp.gain = 0.00002
    vclamp.saturation = 1000        # unitless
    pid = moose.PIDController(path+"/pid")
    #pid.gain = 1.0e-6   # around 1/Rinput of cell
    pid.gain = 1.0/compt.Rm
    print( 'pid.gain = ', pid.gain )
    pid.tauI = 20e-6
    pid.tauD = 5e-6
    pid.saturation = 1000        # unitless
    # Connect voltage clamp circuitry
    moose.connect(lowpass, "output", vclamp, "plusIn")
    moose.connect(vclamp, "output", pid, "commandIn")
    # Holding command potential should come into lowpass on inject
    print( lowpass.dt, vclamp.dt, pid.dt )
    print( lowpass.tick, vclamp.tick, pid.tick )

    moose.connect( compt, 'VmOut', pid, 'sensedIn' )
    moose.connect( pid, 'output', compt, 'injectMsg' )
    moose.reinit()

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
    parser.add_argument( '-m', '--model', type = str, help='Optional: model filename, .g or .xml', default = "models/synSynth7.g" )
    parser.add_argument( '-d', '--dump_subset', type = str, help='Optional: dump selected subset of model into named file', default = "" )
    parser.add_argument( '-hp', '--hide_plot', action="store_true", help='Hide plot output of simulation along with expected values. Default is to show plot.' )
    parser.add_argument( '-hs', '--hide_subplots', action="store_true", help='Hide subplot output of simulation. By default the graphs include dotted lines to indicate individual quantities (e.g., states of a molecule) that are being summed to give a total response. This flag turns off just those dotted lines, while leaving the main plot intact.' )
    args = parser.parse_args()
    innerMain( args.script, modelFile = args.model, dumpFname = args.dump_subset, hidePlot = args.hide_plot, hideSubplots = args.hide_subplots )


def innerMain( script, modelFile = "model/synSynth7.g", dumpFname = "", hidePlot = True, hideSubplots = False ):
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    modelWarning = ""
    modelId = ""
    expt, stims, readouts, model = loadTsv( script )
    if stims[0].field == 'Vclamp':
        if not readouts[0].field == 'Im':
            raise SimError( "Vclamp stimulus must be accompanied by readout field 'Im'. Was: '{}'".format( readouts[0].field ) )
    model.fileName = modelFile
    #This list holds the entire models Reac/Enz sub/prd list for reference
    erSPlist = {}
    # First we load in the model using EE so it is easier to tweak
    try:
        if not os.path.isfile(model.fileName):
            raise SimError( "Model file name {} not found".format( model.fileName ) )
        filename, file_extension = os.path.splitext(model.fileName)
        if file_extension == '.xml':
            modelId, errormsg = moose.mooseReadSBML( model.fileName, 'model', 'ee' )
        elif file_extension == '.g':
            modelId = moose.loadModel( model.fileName, 'model', 'ee' )
        # moose.delete('/model[0]/kinetics[0]/compartment_1[0]')
        elif file_extension == '.py':
            # Assume a moose script for creating the model. It must have a
            # function load() which returns the id of the object containing
            # the model. At this point the model must be in the current dir
            mscript = __import__( filename )
            modelId = mscript.load()


        for f in moose.wildcardFind('/model/##[ISA=ReacBase],/model/##[ISA=EnzBase]'):
            erSPlist[f] = {'s':len(f.neighbors['sub']), 'p':len(f.neighbors['prd'])}
        # Then we apply whatever modifications are specified by user or protocol

        modelWarning = ""
        model.modify( modelId, erSPlist,modelWarning )
        if len(dumpFname) > 2:
            if dumpFname[-2:] == '.g':
                moose.mooseWriteKkit( modelId.path, dumpFname )
            elif len(dumpFname) > 4 and dumpFname[-4:] == '.xml':
                moose.mooseWriteSBML( modelId.path, dumpFname )
            else:
                raise SimError( "Subset file type not known for '{}'".format( dumpFname ) )

        model.buildModelLookup()

        if not hidePlot:
            makeReadoutPlots( readouts, model.modelLookup )


        if stims[0].field == 'Vclamp':
            if not readouts[0].field == 'Im':
                raise SimError( "Vclamp stimulus must be accompanied by readout field 'Im'. Was: '{}'".format( readouts[0].field ) )
            buildVclamp( stims[0], model.modelLookup )
            #Then build the solver with a flag to say rebuild the hsolve.
            buildSolver( modelId, model.solver, useVclamp = True )
        else:
            buildSolver( modelId, model.solver )
        for i in range( 10, 20 ):
            moose.setClock( i, 0.1 )

        score = runit( expt, model,stims, readouts, modelId )
        if not hidePlot:
            print( "Score = {:.3f} for\t{}".format( score, os.path.basename(script) ) )
            for i in readouts:
                pylab.figure(1)
                i.displayPlots( script, model.modelLookup, stims[0], hideSubplots, expt.exptType )
                
            if moose.exists( '/model/plots/vclampCurr' ):
                pylab.figure()
                pylab.plot( moose.element( '/model/plots/vclampCurr' ).vector )
                pylab.title( 'vclamp Current' )
                pylab.figure()
                pylab.plot( moose.element( '/model/plots/Vm' ).vector, label='Vm' )
                pylab.plot( moose.element( '/model/plots/Vhold' ).vector, label='Vhold' )
                pylab.title( 'vclamp Vm' )
            pylab.show()
        moose.delete( modelId )
        return score
        
    except SimError as msg:
        if modelId:
            moose.delete( modelId )
        print( "Error: findSim failed for script {}: {}".format(script, msg ))
        return -1.0
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
