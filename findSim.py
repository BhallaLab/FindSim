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
# 
# Code:
# Figure out how to convert a given molecule to buffered for doing dose-resp
# To do: Provide a way to set model modifications
# Provide way to plot on log scale if dose-response
# Put in stuff with respect to a ratio


# Feb12 2018: Taken from Upi's labnotes autsim12.py and manipulate for the current excel sheet

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

2018
#check if stimulus quantityUnits is blank in excel sheet it shd take mM which was not taking
Apr 18:
    duplicate code is deleted/cleaned up
    RatioRefValue's value is devided after the loop which ensure that the division is done for all the values from zero to endtime
Apr 10:
    clean up in timeUnits and quantityUnits for blank, space etc
    runit: check are made for condition for useSum and useRatio if satifies then moved further
           Also created a dictionaries for stimuli, readout and reference Molecules which is passed
           to parseAndRun and parseAndRunDoser
           cleaned RunDoser and runReferenceDoser 
           
Apr 2:
    Added runInitialReferenceDoser code
    added runRatioDoser code
Mar29: 
    Added Dose-Response code
Mar28:
    cleaned up in parseAndRun for running when useSum and useRation is true
Mar 25:
    stimulus,readout,reference molecules in modelmapping are in list, Equivalent molcules from stimulus,readout block are picked
    up as per index order from the modelmapping: stimulusMolecules, readoutMolecules,referenceMolecule
    changes made in parseAndRun for the same, now its queries index vice
    Model's who run the script should make sure that order is same
    checked for MMenz in pruneDanglingObj 
Mar 17:
    checked for 
        dangling Reac/Enz, 
        if sub/prd is altered RateLaw
        if func's input have chaged
Mar 16: 
    string checked for comma, 
    function to check unique Id is provided in modelmapping
    object's deleted specified in itemstodelete section
    object's deleted specified in modelSubset
        groups and group/object is specified then group is saved
        group/object is mentioned then in group is saved, then object which are 
        set in modelSubseting those are deleted
        same with comparment's,if comparment is specified then sharedobject and group is saved
        else comparement is deleted

#To be checked: 
    #if comparement has just one pool present, while applying the stoich in buildSolver , we get seg fault "installAndUnschedFunc".
    # While checking compartment, checked for CubeMesh or cyclMesh in further if it come through rdesigner check
    # while setting the values like kcat, km etc not taken care for units unlike for concInit
    # check after surviour group, check anything is dangling, like reaction and enzyme if S delete and function check input and out and input with numVars
    # stimuti block is not necessary we can delete entire block or block exist make sure what every empty it doesn't affect the model  
    # different type if time-series types at this point no check is make
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
convertTimeUnits = {('sec','s') : 1.0, ('ms','millisec') : 1e-3,('us','microsec') : 1e-6, ('ns','nanosec') : 1e-9,
                    ('min','m') : 60.0, ('hours','hrs') : 3600.0, "days": 86400.0}
convertConcUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 'nM':1.0e-6, 'pM': 1.0e-9, 'number':1.0, 'ratio':1.0}

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
            exptSource = 'paper', # Options are paper, inHouse, database
            citationId = '',  # Journal name/ in-house project name/ database
            authors = '',   # Who did the work
            journal = ''     # journal
        ):
        self.exptSource = exptSource
        self.citationId = citationId
        self.authors = authors
        self.journal = journal

    def load( fd ):
        arg = [''] * 4
        for line in fd:
            cols = line.split('\t')
            if len( cols ) == 0:
                break
            if cols[0] == "Experiment context":
                break
            for i in range( len( Experiment.argNames ) ):
                if keywordMatches( cols[0], Experiment.argNames[i] ):
                    try:
                        arg[i] = cols[1]
                    except IndexError:
                        arg[i] = ""
                    continue
        return Experiment( arg[0], arg[1], arg[2], arg[3] )
    load = staticmethod( load )

Experiment.argNames = ['exptSource', 'citationId', 'authors', 'journal' ]

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
            stimulusType = 'timeSeries',
            timeUnits = 's',
            quantityUnits = 'mM',
            molecules = [],
            field = '',
            settleTime = 300.0, 
            data = []
        ):
        self.stimulusType = stimulusType
        """This is the most elementary stimulus: assign some model 
        value at a succesion of points in time. Other options are
        timeSeriesWithRestart, doseResponse, and more.
        """
        if timeUnits != " ":
            self.timeUnits = timeUnits
        """timeUnits may be us, ms, s, min, hours, days"""
        #self.timeScale = convertTimeUnits[ timeUnits ]
        self.timeScale = next(v for k, v in convertTimeUnits.items() if timeUnits in k)
        """timeScale is timeUnits scaled to seconds"""
        if quantityUnits and quantityUnits.strip():
            self.quantityUnits = quantityUnits
        else:
            self.quantityUnits = 'mM'
        """Quantity Units may be: M, mM, uM, nM, pM, number, ratio"""
        self.concScale = convertConcUnits[ self.quantityUnits ]
        """concScale is quantityUnits scaled to mM"""
        #self.useRatio = useRatio
        #self.ratioReferenceTime = ratioReferenceTime
        """Timepoint at which to sample the quantity to use as a reference for calculating the ratio"""
        self.molecules = molecules
        """Name of the model entity to modify for the stimulus. 
        Typically a molecule name."""
        self.field = field
        """Name of the field associated with the entity. A bit of an
        unclean entry at this point but later we can fine-tune"""
        self.settleTime = float( settleTime )
        """For dose response, we can specify how long to settle at 
        each level. A value of 0 or less means to automatically go 
        on till steady-state."""
        self.data = data
        """List of pairs of numbers, [time, quantity]"""
        
    def load( fd ):
        arg, data, param, struct, stim, readout, refentMol, ent, refent = innerLoad( fd, Stimulus.argNames, 2 )
        stim = Stimulus( **arg )
        for i in ent:
            stim.molecules=ent
        stim.data = data
        if len(stim.data) != 0:
            if stim.data[0][0] =="settleTime":
                stim.settleTime = stim.data[0][1]
        return stim

    load = staticmethod( load )

Stimulus.argNames = ['timeUnits', 'quantityUnits', 'molecules', 'field', 'settleTime']

##########################################################################

class Readout:
    """Specifies readouts to be obtained from a specific component of 
    the model in the course of the simulated experiment. Almost always
    molecule quantity, but later might be electrical things like membrane 
    potential.
    There can be multiple readouts during an experiment.
    """
    def __init__( self,
            readoutType = 'timeSeries',
            timeUnits = 's',
            quantityUnits = 'mM',
            useRatio = False,
            useSum = False,
            useNormalization=False,
            ratioReferenceTime = 0.0,
            ratioReferenceDose = 0.0,
            molecules = '',
            ratioReferenceEntity = '',
            field = '',
            experimentalReadout = '',
            useXlog = False,
            useYlog = False,
            scoringFormula = 'abs(1-(sim+1e-9)/(expt+1e-9))',
            data = []
            ):
        self.readoutType = readoutType
        """This defines what kind of data is in the readout. 
        timeSeries is the most elementary readout: Monitor a model
        value at a succesion of points in time. Other options are
        doseResponse, and more.
        """
        self.timeUnits = timeUnits
        """timeUnits may be us, ms, s, min, hours, days"""
        self.timeScale = next(v for k, v in convertTimeUnits.items() if timeUnits in k)
        """timeScale is timeUnits scaled to seconds"""
        self.quantityUnits = quantityUnits
        """Quantity Units may be: M, mM, uM, nM, pM, number, ratio"""
        self.concScale = convertConcUnits[ quantityUnits ]
        """concScale is quantityUnits scaled to mM"""
        if useRatio != "":
            self.useRatio = str2bool(useRatio)
        else:
            self.useRatio = useRatio
        if useSum != "":
            self.useSum = str2bool(useSum)
        else:
            self.useSum = False
        if useXlog != "":    
            self.useXlog = str2bool(useXlog)
        else:
            self.useXlog = str2bool(useXlog)
        if useYlog != "":    
            self.useYlog = str2bool(useYlog)
        else:
            self.useYlog = str2bool(useYlog)
        self.useNormalization = str2bool(useNormalization)
        
        self.molecules = molecules
        """Name of the model entity to read. Typically a molecule name."""
        self.experimentalReadout = experimentalReadout
        """Name of the field associated with the entity. A bit of an
        unclean entry at this point but later we can fine-tune"""
        self.ratioReferenceEntity = ratioReferenceEntity
        """Object to use as a reference for computing the readout ratio."""
        self.ratioReferenceTime = float( ratioReferenceTime )
        self.ratioReferenceDose = float( ratioReferenceDose )
        """Timepoint at which to sample the quantity to use as a reference for calculating the ratio. -1 means to sample reference each time we sample the readout, and to use the instantaneous ratio."""
        #self.scoringFormula = scoringFormula
        """Formula to use to score how well the model matches expt"""
        self.data = data
        """List of triplets of numbers, [time, quantity, stderr]"""
        
    def load( fd ):
        arg, data, param, struct, stim, readout, refentMol, ent, refent  = innerLoad( fd, Readout.argNames, 3 )
        readout = Readout( **arg )
        # for i in ent:
        #     readout.entity=ent
        for i in refent:
            readout.ratioReferenceEntity=refent
        readout.data = data
        return readout
    load = staticmethod( load )

Readout.argNames = ['readoutType', 'timeUnits', 'quantityUnits', 
        'useRatio', 'useXlog', 'useYlog', 'useSum', 'useNormalization', 'molecules', 'experimentalReadout', 
        'ratioReferenceTime', 'ratioReferenceDose','ratioReferenceEntity']

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
        self.stimulusMolecules = []
        self.readoutMolecules = []
        self.referenceMolecule = []
        self.scoringFormula = scoringFormula

    def load( fd ):
        '''
        Model::load builds a model instance from a file and returns it.
        '''
        arg, data, param, struct, stim, readout, refentMol, ent, refent  = innerLoad( fd, Model.argNames )
        
        model = Model( **arg )
        for i in param:
            model.addParameterChange( i[0], i[1], i[2] )
        for j in struct[:]:
            #model.addStructuralChange( i[0], i[1] )
            model.addStructuralChange(j.lstrip(),"delete")
        #stimulus molecules  
        model.stimulusMolecules = stim
        #readoutModlecules
        model.readoutMolecules = readout
        
        model.referenceMolecule = refentMol
        
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
        # if change == 'delete':
        #     self.StructuralChange.append( ( entity, change ) )
        # else:
        #     print( "Warning: Model::addStructuralChange: Unknown modification: " + change )
    def findObj( self,rootpath, name ):
        '''
        Model:: findObj causes to search unqiue id provided in modelmapping's 
        modelSubset,stimulusMolecules,readoutMolecules,itemstodelete,parameterChange
        if more than one value is returned then program halts unless user correct this.
        Expected min unique id, if found more than one, then its parent needs to be passed until
        a unique is found (This is b'cos in moose, all the object's are path based)
        '''
        try1 = moose.wildcardFind( rootpath+'/' + name )
        try2 = moose.wildcardFind( rootpath+'/##/' + name )
        #print " findObj ",rootpath+'/'+name, moose.wildcardFind(rootpath+'/'+name)
        #print " findObj 2",rootpath+'/##/'+name, moose.wildcardFind(rootpath+'/##/'+name)
        if len( try1 ) + len( try2 ) > 1:
            #print( "Bad: Too many entries. ", try1, try2)
            return moose.element('/'), ( "Bad: Too many entries. ", try1, try2)
        if len( try1 ) + len( try2 ) == 0:
            #print( "Bad: zero entries. ", name )
            return moose.element('/'),( "Bad: zero entries. ", name )
        if len( try1 ) == 1:
            return try1[0],""
        else:
            return try2[0],""

    def modify( self, modelId, erSPlist, odelWarning):
        # Start off with things explicitly specified for deletion.
        kinpath = modelId.path
        if self.itemstodelete:
            for ( entity, change ) in self.itemstodelete[:]:
                if entity != "":
                    foundobj,errormsg = self.findObj(kinpath, entity)
 
                    if moose.element(foundobj).className == "Shell":
                       raise SimError("modify: " + ', '.join(map(str, errormsg)))
                    else:
                        if moose.exists( moose.element(foundobj).path ):
                            obj = moose.element( foundobj.path )
                            if change == 'delete':
                                if obj.path != modelId.path and obj.path != '/model[0]':
                                    moose.delete( obj )
                                else:
                                    raise SimError("modelId/rootPath is not allowed to delete {}".format( obj) )
                        else:
                            raise SimError("Object does not exist {}".format( entity ) )
                
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
                foundobj = ""
                foundobj, errormsg = self.findObj(kinpath, i)
                if moose.element(foundobj).className == "Shell":
                    raise SimError("Model Subsetting" + ', '.join(map(str, errormsg)))
                else:
                    if moose.exists( moose.element(foundobj).path ):
                        elm = moose.element( moose.element(foundobj).path  )
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
                    else:
                        print("Warning: subset entry '{}' not found".format(i))
            
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
                foundobj,errormsg = self.findObj(kinpath, entity)
                if moose.element(foundobj).className == 'Shell':
                    raise SimError("ParameterChange: "+ ', '.join(map(str, errormsg)))
                else:
                    if moose.exists( moose.element(foundobj).path ):
                        obj= moose.element( foundobj.path )
                        if field == "concInit (uM)":
                            field = "concInit"
                        #print " obj ", obj, field, value
                        moose.element( obj ).setField( field, value )
                        # if field == "concInit (uM)":
                        #     print obj.concInit
                        #     moose.element( obj ).setField( "concInit", value )
                        #     print " after ",obj.concInit
                        # else:

            #Function call for checking dangling Reaction/Enzyme/Function's
            pruneDanglingObj( kinpath, erSPlist)
            
Model.argNames = ['modelSource', 'citation', 'citationId', 'authors',
            'modelSubset','stimulusMolecules', 'readoutMolecules','referenceMolecule', 'fileName', 'solver', 'notes' ,'scoringFormula','itemstodelete','parameterChange']

#######################################################################
def list_to_dict(rlist):
    return dict(map(lambda s : s.split(':'), rlist))

def innerLoad( fd, argNames, dataWidth = 2):
    data = []
    param = []  # list of tuples of objname, field, value.
    arg = {}
    struct = []
    stim = []
    readout = []
    ent = []
    refent = []
    refentMol = []
    for line in fd:
        cols = line.split( "\t" )
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            return arg, data, param, struct, stim, readout, refentMol, ent, refent 

        if keywordMatches( cols[0], 'stimulusMolecules' ):
            if cols[1] != "":
                #stim = dict(map(lambda s : s.split(':'), cols[1].split(',')))
                stim = cols[1].split(',')
        
        if keywordMatches( cols[0], 'readoutMolecules' ):
            if cols[1] != "":
                #readout = dict(map(lambda s : s.split(':'), cols[1].split(',')))
                readout = cols[1].split(',')
        
        if keywordMatches( cols[0], 'referenceMolecule' ):
            #readout=cols[1].split(',')
            if cols[1] != "":
                #refentMol = dict(map(lambda s : s.split(':'), cols[1].split(',')))
                refentMol = cols[1].split(',')
        
        if keywordMatches( cols[0], 'ratioReferenceEntity' ):
            refent=cols[1]#.split(',')
            #print "ratioReferenceENTITY",refent

        if keywordMatches( cols[0], 'Data' ):
            readData( fd, data, dataWidth )

            #print "Ret READ DATA from INNERLOAD", len( data )
            return arg, data, param, struct, stim, readout, refentMol, ent, refent 

        for i in argNames:
            if keywordMatches( cols[0], i ):
                arg[i] = str.strip( nonBlank( cols) )
                continue;
        if keywordMatches(cols[0],"parameterChange"):
            readParameter(fd,param,dataWidth)

        if keywordMatches( cols[0], 'itemstodelete' ):
            struct= cols[1].split(',')

    return arg, data, param, struct, stim, readout, refentMol, ent, refent 

def nonBlank( cols ):
    for i in cols[1:]:
        if i != '':
            return i
    return ''

def readData( fd, data, width ):
    for line in fd:
        cols = line.split("\t" )
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            break
        if cols[0].lower() == "time" or cols[0].lower() == "dose":
            continue
        row = []
        for c in cols:
            if c != '':
                #check what datatypes 
                #row.append( ( re.sub('[^A-Za-z0-9.]+', '', c) ) )
                row.append(c)
                if len( row ) >= width:
                    break;
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
        raise SimError (" \nWarning: Found dangling Reaction/Enzyme, if this/these reac/enz to be deleted then add in the excelsheet in ModelMapping -> itemstodelete section. Program will exit for now. "+mWarning)
    if ratelawchanged:
        raise SimError ("\nWarning: This reaction or enzyme's RateLaw needs to be corrected as its substrate or product were deleted while subsetting. Program will exit now. \n"+mRateLaw)
    if funcIPchanged:
        raise SimError ("\nWhile subsetting the either one or more input's to the function is missing, if function need/s to be deleted  then add this/these in the excelsheet in ModelMapping -> itemstodelete section or one need to care to bring back those molecule/s, program will exit now.\n"+mFunc)
    
##########################################################################
def parseAndRun( model, stims, stimuliMaptoMolMoose, readouts, readoutsMaptoMolMoose, ratioRefMaptoMolMoose, modelId ):
    score = 0.0
    q       = []
    stdError  = []
    
    plots = {}
    tabl  = {}
    numScore  = 0
    clock = moose.element( '/clock' )
    ##################If extra plots need, populate extraplots list ###########################
    # extraplots=[]
    # dp = moose.Neutral('/model/graph1')
    # for i in extraplots:
    #     extraplt,errormsg= model.findObj('/model',i)
    #     if moose.element(extraplt).className == "Shell":
    #         #This check is for multiple entry
    #         print ("Extra plots: ",errormsg)
    #         exit()
    #     else:
    #         if not moose.exists( extraplt.path ):
    #             print( "Error: Object does not exist: '" + i + "'")
    #             quit()
    #         else:
    #             moose.connect(moose.Table2((d.path+'/'+(moose.element(extraplt)).name)+'.Co'),'requestOut',moose.element(extraplt),'getConc')
    # scoreTab = { i.entity: [[],[],[]] for i in readout }
    ##################### End #################################################
    for i in stims:
        for j in i.data:
            if j[0] =="settleTime":
                j[0] = i.settleTime
            heapq.heappush( q, (float(j[0])*i.timeScale, [i, float(j[1])*i.concScale ] ) )
    
    for i in readouts:
        readoutMol = readoutsMaptoMolMoose[i][i.molecules]
        for mReadout in readoutMol:
            ########################Creating table's for plotting for full run ################################################
            plotstr = modelId.path+'/plots/' + ntpath.basename(mReadout.name) + '.Co'
            tabl[mReadout.name] = moose.Table2(plotstr)
            moose.connect( tabl[mReadout.name],'requestOut',mReadout,'getConc' )
            t_dt = moose.element( modelId.path+'/plots/' + ntpath.basename(mReadout.name) + '.Co' )
            ####################################################################################################################
            plots = {plotstr: PlotPanel(i)}
        for j in i.data:
            if j[0] =="settleTime":
                j[0] = i.settleTime
            heapq.heappush( q, (float(j[0])*i.timeScale, [i, float(j[1])*i.concScale ] ) )
            stdError.append(float(j[2]))
        if ratioRefMaptoMolMoose:  
            if ratioRefMaptoMolMoose[i][i.ratioReferenceEntity]:
                t = 0
                t = i.ratioReferenceTime * i.timeScale
                heapq.heappush( q, (t, [i, -1] ) )

    readoutMolsReadout = []
    readoutRefReadout = []
    moose.reinit()
    ratioRefVal = 1
    sumsl = []
    xptslist = []
    exptlist = []  
    list_of_lists = []
    sumslist = []
    tab = []
    for i in range( len( q ) ):
        ref=0.0
        ratioRefValues = 0

        t, event = heapq.heappop( q )
        val = event[1]
        sim = 0.0
        currt = clock.currentTime
        #print q, t, event
        if ( t > currt ):
            moose.start( t - currt )
        if isinstance( event[0], Stimulus ):
            s = event[0]
            if stimuliMaptoMolMoose[s]:
                if stimuliMaptoMolMoose[s][s.molecules]:
                    stimMol = stimuliMaptoMolMoose[s][s.molecules]
                    for sm in stimMol:
                        if t == 0:
                            ##At time zero we initial the value concInit or nInit
                            if s.field == 'conc':
                                sm.setField("concInit",val)
                                moose.reinit()
                            elif s.field == "n":
                                sm.setField( 'nInit', val )
                            else:
                                raise SimError("\""+ s.field+"\" specified field name in Stimuli->field name is not valid field in moose ")
                        else:
                            sm.setField( s.field, val )
        elif isinstance( event[0], Readout ):
            if not ( val < 0 ): expt = val
            ''' 
            1. if ratioReferenceTime is < zero,
                -then RatioReferenceEntity should calculated at every time point i.e at every readout time point the ration shd be taken
                and this should be applied to readoutmoleucle values while calculating the ratio sim/ratioRefMol
            2. if ratioReferenceTime is zero then take concInit of molecule at time zero
            3. if ratioReferenceTime > 0 calculate at ratioReferenceTime point 
             readoutvalues/rrValue
            '''
            if event[1] == -1:
                #event[1] returns -1 then this is for getting RationReferencevalue
                for rrM in ratioRefMaptoMolMoose[event[0]][event[0].ratioReferenceEntity]:
                    ratioRefValues+=moose.element(rrM).getField(event[0].experimentalReadout)
                ratioRefVal = ratioRefValues
            else:
                r = event[0]
                if readoutsMaptoMolMoose[r]:
                    if readoutsMaptoMolMoose[r][r.molecules]:
                        readoutMol = readoutsMaptoMolMoose[r][r.molecules]
                        for outputmol in readoutMol:
                            sim+= outputmol.getField(r.experimentalReadout)
                if r.useRatio:
                    if r.ratioReferenceTime < 0.0:
                        # Compute ratio reference every time data is sampled.
                        for rrM in ratioRefMaptoMolMoose[event[0]][event[0].ratioReferenceEntity]:
                            ratioRefValues += moose.element(rrM).getField(event[0].experimentalReadout)
                        ratioRefVal.append(ratioRefValues)

                    if r.ratioReferenceTime == 0.0:
                        # Take concInit as ratio reference.
                        for rrM in ratioRefMaptoMolMoose[event[0]][event[0].ratioReferenceEntity]:
                            ratioRefValues += moose.element(rrM).getField('concInit')
                        ratioRefVal = ratioRefValues
                    if r.ratioReferenceTime > 0.0 and val < 0:
                        # Compute ratio reference only at specified time.
                        ratioRefVal = ratioRefValues
                        # Don't do any calculation of score for this queue entry
                        continue
                    #sim /= ratioRefVal
                xptslist.append( t )
                exptlist.append( expt/r.concScale )
                sumsl.append( sim/r.concScale )
    #This is done bcos the ratioRefVal will be divided to all the values instead of value after RatioReferenceTime
    suml1 = []
    suml1 = [x / ratioRefVal for x in sumsl]
    sumsl = suml1
    del(suml1)

    for i in readouts:
        ###############################################################################################################
        if readoutsMaptoMolMoose[r]:
            if readoutsMaptoMolMoose[r][r.molecules]:
                readoutMol = readoutsMaptoMolMoose[r][r.molecules]
                for outputmol in readoutMol:
                    list_of_lists.append((tabl[outputmol.name].vector).tolist())
        ###############################################################################################################
        tab_values = [(sum(x)/(i.concScale)) for x in zip(*list_of_lists)]
        tab_vals = [j/ratioRefVal for j in tab_values]

        for m in range(0,len(sumsl)):
            if i.useNormalization:
                sim=sumsl[m]/sumsl[0]
            else:
                sim=sumsl[m]
            expt=exptlist[m]
            sc = eval( model.scoringFormula )
            score += sc
            numScore += 1
            sumslist.append(sim)
        for k in range(0,int(xptslist[-1])):
            if i.useNormalization:
                tab.append(tab_values[int(k/t_dt.dt)]/tab_values[int(xptslist[0]/t_dt.dt)])
            else:
                tab.append( tab_vals[int(k/t_dt.dt)] )

    ###############################################################################################################
    time_full=numpy.arange( 0, xptslist[-1] )
    # for i in range(int(time_full[0]/t_dt.dt),int(time_full[-1]/t_dt.dt)+1):
    #     tab_full.append(tab[i])
    full_run=[tab,time_full]
    ###############################################################################################################
    for key in plots:
        plots[key].sim = sumslist
        plots[key].xpts = xptslist
        plots[key].expt = exptlist
        plots[key].yerror = stdError
    pylab.figure(1)
    

    pylab.plot(full_run[1],full_run[0], 'r--', linewidth=3 )
    if numScore > 0:
        return score / numScore, plots#, full_run#, addFigs_vals
    return 0, plots, #full_run#, addFigs_vals


##########################################################################
def parseAndRunDoser( model,stims, stimuliMaptoMolMoose, readouts, readoutsMaptoMolMoose, ratioRefMaptoMolMoose, modelId ):
    
    if len( stims ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs exactly one stimulus molecule, {} defined".format( len( stims ) ) )
    if len( readouts ) != 1:
        raise SimError( "parseAndRunDoser: Dose response run needs exactly one readout molecule, {} defined".format( len( readout ) ) )
    numLevels = len( readouts[0].data )
    
    if numLevels == 0:
        raise SimError( "parseAndRunDoser: no dose (stimulus) levels defined for run" )
    
    runTime = float(stims[0].settleTime)
    
    if runTime <= 0.0:
        print( "Currently unable to handle automatic settling to stead-state in doseResponse, using default 300 s." )
        runTime = 300
    
    doseMol = ""
    #Stimulus Molecules
    #Assuming one stimulus block, one molecule allowed
    doseMol = stimuliMaptoMolMoose[stims[0]][stims[0].molecules][0]
    for r in readouts:
        ent=""
        if readoutsMaptoMolMoose[r]:
            if readoutsMaptoMolMoose[r][r.molecules]:
                readoutMol = readoutsMaptoMolMoose[r][r.molecules]
                for readMol in readoutMol:
                    ent += readMol.name
                    ent += " "
                    #IS plot for dose response is in stimMol?
                    plots = { ent: PlotPanel( r, moose.element(doseMol).name + ' ({})'.format( stims[0].quantityUnits ) )}
        ### RatioReferenceEntity

        if len(ratioRefMaptoMolMoose):
            if ratioRefMaptoMolMoose[r][r.ratioReferenceEntity]:
                readoutreferenceMol = ratioRefMaptoMolMoose[r][r.ratioReferenceEntity]

        if not r.useRatio:              
            return runDoser(model,plots, stims[0],doseMol, r, readoutsMaptoMolMoose, ratioRefMaptoMolMoose,ent) # Use absolute quantities 
        elif r.ratioReferenceTime >= 0:
            return runReferenceDoser ( model,plots, stims[0],doseMol,r,readoutsMaptoMolMoose, ratioRefMaptoMolMoose, ent)
        
##########################################################################
def runDoser( model, plots, stim, doseMol, readout, readoutsMaptoMolMoose,ratioRefMaptoMolMoose,ent ):
    score = 0.0
    stdError=[]   
    responseScale = readout.concScale
    doseScale = stim.concScale
    runTime = float(stim.settleTime)
    sim = 0.0
    for dose, response, stderr in readout.data:
        stdError.append(float(stderr))
        dose = float(dose)
        doseMol.concInit = dose * doseScale
        moose.reinit()
        moose.start( runTime )
        if readout.useSum:
            for r in readoutsMaptoMolMoose[readout][readout.molecules]:
                sim += r.getField( readout.experimentalReadout )
        else:
            sim = readoutsMaptoMolMoose[readout][readout.molecules][0].getField( readout.experimentalReadout)

        expt = float(response) * responseScale
        score += eval( model.scoringFormula )
        plots[ent].xpts.append( dose )
        plots[ent].sim.append( sim / responseScale )
        plots[ent].expt.append( expt / responseScale )
        plots[ent].yerror = stdError
    return score / len(readout.data), plots

#################################################################
def runReferenceDoser( model, plots, stim,stimMol, iofReadout,readoutMaptoMooseMol,ratioReferenceMol, ent ):
    score = 0.0
    reference=0.0
    stdError=[]
    doseMol = stimMol
    doseScale = stim.concScale
    runTime = float(stim.settleTime)
    
    if iofReadout.ratioReferenceDose>=0.0:
        doseMol.concInit = iofReadout.ratioReferenceDose * doseScale
    else:
        doseMol.concInit = iofReadout.data[0][0] * doseScale
    moose.reinit()

    referenceMol = ratioReferenceMol[iofReadout]
    for k in referenceMol[iofReadout.molecules]:
        moose.reinit()
        if iofReadout.ratioReferenceTime == 0:
            reference += k.getField('concInit')
            continue
        else:
            moose.start( iofReadout.ratioReferenceTime)
            reference += k.getField( iofReadout.experimentalReadout)
    
    for dose, response, stderr in iofReadout.data:
        sim = 0.0
        #stdError.append(stderr)
        dose = float(dose)
        stdError.append(float(stderr))
        doseMol.concInit = float(dose) * doseScale
        moose.reinit()
        moose.start( runTime )
        #readoutMolecule = readoutMaptoMooseMol[iofReadout]
        readoutsMolecules = readoutMaptoMooseMol[iofReadout][iofReadout.molecules]
        for i in readoutsMolecules:
            sim += i.getField( iofReadout.experimentalReadout )
        sim = float(sim / reference)
        expt = float(response)
        score += eval( model.scoringFormula )
        plots[ent].xpts.append( dose )
        plots[ent].sim.append( sim )
        plots[ent].expt.append( expt )
        plots[ent].yerror = stdError
    return score / len(iofReadout.data), plots#, full_run

##########################################################################
##########################################################################

class PlotPanel:
    def __init__( self, readout, xlabel = '' ):
        self.name=[]


        for i in readout.molecules:
            self.name.append(ntpath.basename(readout.molecules))
        self.exptType = readout.readoutType
        self.useXlog = readout.useXlog
        self.useYlog = readout.useYlog
        if len( xlabel ) > 0:
            self.xlabel = xlabel
        else:
            self.xlabel = 'Time ({})'.format( readout.timeUnits )

        self.xpts = []
        self.sim = []
        self.expt = []
        self.yerror = []
        self.sumName=""
        for i in self.name:
            self.sumName += i
            self.sumName += " "
            self.ylabel = i+' ({})'.format( readout.quantityUnits ) #problem here.check so that y-axis are for diff plts not in one plot

    def plotme( self,excelsheet ):
        if self.useXlog:
            if self.useYlog:
                #pylab.loglog( self.xpts, self.expt, label = self.sumName + '_expt' )
                pylab.loglog( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                #for i in range( len( self.name ) ):
                #pylab.loglog( self.xpts, self.sim, label = self.sumName + '_sim' )
                pylab.loglog( self.xpts, self.sim, 'ro', label = 'sim', linewidth='2' )
            else:
                #pylab.semilogx( self.xpts, self.expt, label = self.sumName +'_expt' )
                pylab.semilogx( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                #for i in range( len( self.name ) ):
                #pylab.semilogx( self.xpts, self.sim, label = self.sumName + '_sim' )
                pylab.semilogx( self.xpts, self.sim, 'ro', label = 'sim', linewidth='2' )
        else:
            if self.useYlog:
                #pylab.semilogy( self.xpts, self.expt, label = self.sumName +'_expt' )
                pylab.semilogy( self.xpts, self.expt, 'bo-', label = 'expt', linewidth='2' )
                #for i in range( len( self.name ) ):
                #pylab.semilogy( self.xpts, self.sim, label = self.sumName + '_sim' )
                pylab.semilogy( self.xpts, self.sim, 'ro', label = 'sim', linewidth='2' )
            else:
                #for i in range( len( self.name ) ):
                #pylab.plot( self.xpts, self.expt, label = self.sumName + '_expt' )
                pylab.plot( self.xpts, self.expt,'bo-', label = 'experiment', linewidth='2' )
                #print " self.yerror ",self.yerror
                pylab.errorbar( self.xpts, self.expt, yerr=self.yerror )
                #pylab.plot( self.xpts, self.sim, label = self.sumName + '_sim' )
                pylab.plot( self.xpts, self.sim, 'ro', label = 'sim', linewidth='2' )

        pylab.xlabel( self.xlabel )
        pylab.ylabel( self.ylabel )
        pylab.title(excelsheet)
        pylab.legend(fontsize="small",loc="lower right")

#############################################################################
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
                        #print "#########################", cols[0]
                    if cols[0] == 'Stimuli':
                        stims.append( Stimulus.load(fd ) )
                        #print "#########################", cols[0]
                    if cols[0] == 'Readouts':
                        readouts.append( Readout.load(fd) )
                        #print "#########################", cols[0]
                    if cols[0] == 'Model mapping':
                        model = Model.load(fd )
                        #print "#########################", cols[0]
    
    # print "expt ", expt.exptSource, expt.citationId, expt.journal, expt.authors
    # for s in stims:
    #     print " \n stims ",s.timeUnits, s.quantityUnits, s.entity,s.field,s.settleTime, s.data,
    # for r in readouts:
    #     print " \n Readout ",r.readoutType, "TU ", r.timeUnits, "QU ",r.quantityUnits,\
    #                     " RATIO", r.useRatio, " SUM ",r.useSum, " NO ",r.useNormalization,\
    #                     "RRT ", r.ratioReferenceTime, "RRD", r.ratioReferenceDose,\
    #                     "MOL", r.molecules," RRE ", r.ratioReferenceEntity,\
    #                     "ER ", r.experimentalReadout, "XL ", r.useXlog, "YL ",r.useYlog,\
    #                     "DATA ",r.data
    # print " \nmodel ",model.modelSource, " \ncit ", model.citation, " \nCITID ",model.citationId, " \nAut: ",model.authors, "\ndetails: ",\
    #                 model.detail, "\nsubset: ",model.modelSubset,"\nFILE: ", model.fileName, " \nsolver: ",model.solver, "\nnotes: ",\
    #                 model.notes, " \nparameterChange: ",model.parameterChange, " \nitemstodelete: ",model.itemstodelete
    return expt,stims,readouts,model

def buildSolver( modelId, solver ):
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

def runit( model,stims, readouts,modelId ):
    doDoser = False
    for i in readouts:
        if keywordMatches( i.readoutType, 'Dose-Response' ) or  keywordMatches( i.readoutType, 'DoseResponse'):
            doDoser = True
    stimuliMaptoMolMoose  = {}
    readoutsMaptoMolMoose = {}
    ratioRefMaptoMolMoose = {}

    stimuliMaptoMolMoose = mapStimdataToMoose(stims,model,modelId)
    
    readoutsMaptoMolMoose,ratioRefMaptoMolMoose = mapReadoutdataToMoose(readouts,model,modelId)
    for i in readouts:
        readoutsMolecules =[]
        ratioMolecules = []
        if i in readoutsMaptoMolMoose:
            if i.molecules in readoutsMaptoMolMoose[i]:
                readoutsMolecules = readoutsMaptoMolMoose[i][i.molecules]
            
        if i in ratioRefMaptoMolMoose:
            if i.ratioReferenceEntity in ratioRefMaptoMolMoose[i]:
                ratioMolecules = ratioRefMaptoMolMoose[i][i.ratioReferenceEntity]

        if i.useSum:
            if not len(readoutsMolecules) >1 and not len(ratioMolecules) >1:
                raise SimError (" Readout->useSum is True but ModelMapping->readoutMolecules or ModelMapping->referenceMolecule has less than two entry. Program will exit")
                
            if i.useRatio:
                if len(ratioMolecules) < 1:
                    raise SimError(" Readout->useRatio is True, expect referenceMolecule in ModelMapping has atleast one entry. Program will exit")
                    
    if doDoser:
        return parseAndRunDoser( model,stims, stimuliMaptoMolMoose, readouts, readoutsMaptoMolMoose, ratioRefMaptoMolMoose, modelId)
    else:
        return parseAndRun( model, stims, stimuliMaptoMolMoose, readouts, readoutsMaptoMolMoose, ratioRefMaptoMolMoose, modelId )

def mapReadoutdataToMoose(readout,model,modelId):
    readoutsMaptoMolMoose = {}
    ratioRefMaptoMolMoose = {}
    for j in readout:
        if len(j.molecules):
            if ',' in j.molecules:
                raise SimError (" Warning: In excel sheet, Readouts->molecules has 2 molecules \""+ j.molecules +"\" which is not allowed in a single Readout block. \n If one wish to keep this seperate out to a seperate Readout block or if this was for summation then use \'+\' sign, progran will exist")
            else:
                try:
                    readoutMolMap = []
                    readoutsMolMaptoMoose = {}
                    modelReadoutMol = model.readoutMolecules[readout.index(j)]
                    if '+' in modelReadoutMol:
                        readoutMolMap = ((modelReadoutMol.replace("\n","")).split('+'))
                    else:
                        readoutMolMap.append(modelReadoutMol.replace("\n",""))
                    for rm in readoutMolMap:
                        mReadout,errormsg = model.findObj(modelId.path,rm)
                        if moose.element(mReadout).className == "Shell":
                            #This check is for multiple entry
                            raise SimError("ModelMapping->Readout Molecule: "+ ', '.join(map(str, errormsg)))
                        else:
                            if not moose.exists( mReadout.path ):
                                raise SimError("Error: Object does not exist: '" + s + "'")
                                
                            else:
                                if j.molecules not in readoutsMolMaptoMoose :
                                    readoutsMolMaptoMoose [j.molecules] = [mReadout]
                                else:
                                    readoutsMolMaptoMoose [j.molecules].append(mReadout)
                    if readoutsMolMaptoMoose:
                        readoutsMaptoMolMoose[j] = readoutsMolMaptoMoose
                except IndexError:
                    pass
        #RatioReferenceMolecules
        if len(j.ratioReferenceEntity):
            if ',' in j.ratioReferenceEntity:
                raise SimError(" Warning: In excel sheet, Readouts->ratioReferenceEntity has 2 molecules \""+ j.ratioReferenceEntity +"\" which is not allowed in a single Readout block. \n If one wish to keep this, seperate out to a seperate Readout block  with ratioReferenceEntity or if this was for summation then use \'+\' sign, progran will exist")
            else:
                try:
                    ratioRefMolMaptoMoose = {}
                    ratioRefMolMap = [] 
                    modelratioRefMol = model.referenceMolecule[readout.index(j)]
                    if '+' in modelratioRefMol:
                        ratioRefMolMap = ((modelratioRefMol.replace("\n","")).split('+'))
                    else:
                        ratioRefMolMap.append(modelratioRefMol.replace("\n",""))
                    for rm in ratioRefMolMap:
                        mRefmol,errormsg = model.findObj(modelId.path,rm)
                        if moose.element(mRefmol).className == "Shell":
                            #This check is for multiple entry
                            raise SimError("ModelMapping->Readout Molecule: ",+ ', '.join(map(str, errormsg)))
                        else:
                            if not moose.exists( mRefmol.path ):
                                raise SimError( "Error: Object does not exist: '" + s + "'")
                            else:
                                if j.ratioReferenceEntity not in ratioRefMolMaptoMoose :
                                    ratioRefMolMaptoMoose [j.ratioReferenceEntity] = [mRefmol]
                                else:
                                    ratioRefMolMaptoMoose [j.ratioReferenceEntity].append(mRefmol)
                    if ratioRefMolMaptoMoose:
                        ratioRefMaptoMolMoose[j] = ratioRefMolMaptoMoose
                except IndexError:
                    pass          
    
    return readoutsMaptoMolMoose,ratioRefMaptoMolMoose

def mapStimdataToMoose(stims,model,modelId):
    stimuliMaptoMolMoose  = {}
    for i in stims:
        if len(i.molecules):
            if ('+' in i.molecules) or (',' in i.molecules):
                raise SimError(" Warning: In excel sheet, Stimuli->molecules has 2 molecules \""+ i.molecules +"\" which is not allowed, progran will exist")
            else:
                stimMolMap = []
                stimuliMolMaptoMoose ={}
                try:
                    modelStimModel = model.stimulusMolecules[stims.index(i)]
                    if '+' in model.stimulusMolecules[stims.index(i)]:
                        stimMolMap = ((model.stimulusMolecules[stims.index(i)].replace('\n', "")).split('+'))
                    else:
                        stimMolMap.append(model.stimulusMolecules[stims.index(i)].replace("\n",""))
                    for sm in stimMolMap:
                        mSource,errormsg= model.findObj(modelId.path,sm)
                        if moose.element(mSource).className == "Shell":
                            #This check is for multiple entry
                            raise SimError ("ModelMapping->Readout Molecule: "+ ', '.join(map(str, errormsg)))
                           
                        else:
                            if not moose.exists( mSource.path ):
                                raise SimError( "Error: Object does not exist: '" + s + "'")
                            else:
                                if i.molecules not in stimuliMolMaptoMoose :
                                    stimuliMolMaptoMoose[i.molecules] = [mSource]
                                else:
                                    stimuliMolMaptoMoose[i.molecules].append(mSource)
                except IndexError:
                    raise SimError( "Warning: model->stimulusMolecules doesn't have entry as many as stimuli block")
            if stimuliMolMaptoMoose:
                stimuliMaptoMolMoose[i] = stimuliMolMaptoMoose
    return stimuliMaptoMolMoose

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
    parser.add_argument( '-m', '--model', type = str, help='Optional: model filename, .g or .xml', default = "FindSim_compositeModel_1.g" )
    parser.add_argument( '-d', '--dump_subset', type = str, help='Optional: dump selected subset of model into named file', default = "" )
    parser.add_argument( '-hp', '--hide_plot', action="store_true", help='Hide plot output of simulation along with expected values. Default is to show plot.' )
    args = parser.parse_args()
    innerMain( args.script, modelFile = args.model, dumpFname = args.dump_subset, hidePlot = args.hide_plot )


def innerMain( script, modelFile = "FindSim_compositeModel_1.g", dumpFname = "", hidePlot = True ):
    #print( "{}, {}, {}, {}".format( script, modelFile, dumpFname, hideDisplay ) )
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    modelWarning = ""
    modelId = ""
    expt, stims, readouts, model = loadTsv( script )
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
        for f in moose.wildcardFind('/model/##[ISA=ReacBase],/model/##[ISA=EnzBase]'):
            erSPlist[f] = {'s':len(f.neighbors['sub']), 'p':len(f.neighbors['prd'])}
        # Then we apply whatever modifications are specified by user or protocol
        moose.Neutral('/model/plots')
        modelWarning = ""
        model.modify( modelId, erSPlist,modelWarning )
        if len(dumpFname) > 2:
            if dumpFname[-2:] == '.g':
                moose.mooseWriteKkit( modelId.path, dumpFname )
            elif len(dumpFname) > 4 and dumpFname[-4:] == '.xml':
                moose.mooseWriteSBML( modelId.path, dumpFname )
            else:
                raise SimError( "Subset file type not known for '{}'".format( dumpFname ) )

        #Then we build the solver.
        buildSolver( modelId, model.solver )
        for i in range( 10, 20 ):
            moose.setClock( i, 0.1 )

        score, plots = runit( model,stims, readouts, modelId )
        if not hidePlot:
            for name, p in plots.items():
                #pylab.figure()
                p.plotme( script )
            pylab.show()
            print( "Script = {}, score = {}".format( script, score ) )
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
