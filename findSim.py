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
import moose
import os
import re

convertTimeUnits = {('sec','s') : 1.0, ('ms','millisec') : 1e-3,('us','microsec') : 1e-6, ('ns','nanosec') : 1e-9,
                    ('min','m') : 60.0, ('hours','hrs') : 3600.0, "days": 86400.0}
convertConcUnits = { 'M': 1e3, 'mM': 1.0, 'uM': 1.0e-3, 'nM':1.0e-6, 
        'pM': 1.0e-9, 'number':1.0, 'ratio':1.0}

def keywordMatches( k, m ):
    return k.lower() == m.lower()

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
        self.timeUnits = timeUnits
        """timeUnits may be us, ms, s, min, hours, days"""
        #self.timeScale = convertTimeUnits[ timeUnits ]
        self.timeScale = next(v for k, v in convertTimeUnits.items() if timeUnits in k)
        """timeScale is timeUnits scaled to seconds"""
        self.quantityUnits = quantityUnits
        """Quantity Units may be: M, mM, uM, nM, pM, number, ratio"""
        self.concScale = convertConcUnits[ quantityUnits ]
        """concScale is quantityUnits scaled to mM"""
        #self.useRatio = useRatio
        #self.ratioReferenceTime = ratioReferenceTime
        """Timepoint at which to sample the quantity to use as a reference for calculating the ratio"""
        self.entity = molecules
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
        arg, data, param,struct,ent,refent = innerLoad( fd, Stimulus.argNames, 2 )
        stim = Stimulus( **arg )
        #stim.data = data
        for i in ent:
            stim.entity=ent
        stim.data = data
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
            molecules = [],
            ratioReferenceEntity = [],
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
        self.useRatio = str2bool(useRatio)
        self.useSum = str2bool(useSum)
        self.useXlog = str2bool(useXlog)
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
        arg, data, param,struct,ent,refent = innerLoad( fd, Readout.argNames, 3 )
        readout = Readout( **arg )
        for i in ent:
            readout.entity=ent
        for i in refent:
            readout.ratioReferenceEntity=refent
        readout.data = data
        return readout
    load = staticmethod( load )

Readout.argNames = ['readoutType', 'timeUnits', 'quantityUnits', 
        'useRatio', 'useXlog', 'useYlog', 'useSum', 'useNormalization', 'molecules', 'experimentalReadout', 
        'ratioReferenceTime', 'ratioReferenceEntity']

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

    def load( fd ):
        '''
        Model::load builds a model instance from a file and returns it.
        '''
        arg, data, param, struct, stim, readOut = innerLoad( fd, Model.argNames )
        
        model = Model( **arg )
        for i in param:
            model.addParameterChange( i[0], i[1], i[2] )
        for j in struct[:]:
            #model.addStructuralChange( i[0], i[1] )
            model.addStructuralChange(j.lstrip(),"delete")
        #stimulus molecules  
        model.stimulusMolecules = stim
        #readoutModlecules
        model.readoutMolecules = readOut


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
        if len( try1 ) + len( try2 ) > 1:
            print( "Bad: Too many entries. ", try1, try2)
            return
        if len( try1 ) + len( try2 ) == 0:
            print( "Bad: zero entries. ", name )
            return 
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
                    foundobj = self.findObj(kinpath, entity)
                    if foundobj:
                        if moose.exists( moose.element(foundobj).path ):
                            obj = moose.element( foundobj.path )
                            if change == 'delete':
                                if obj.path != modelId.path and obj.path != '/model[0]':
                                    moose.delete( obj )
                                else:
                                    print ("modelId/rootPath is not allowed to delete ", obj)
                        else:
                            print "Object does not exist ", entity
                    else:
                        exit()
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
                foundobj = self.findObj(kinpath, i)
                if foundobj:
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
            for l in allCompts:
                elmCmpt = set(moose.wildcardFind(l.path+'/#[ISA=PoolBase]'+','+ l.path+'/#[ISA=ReacBase]'))
                deleteObjsfromCompt = list(elmCmpt-nonComptSet)
                deleteObjsfromCompt = [i for i in deleteObjsfromCompt if not isinstance(moose.element(i.parent), moose.EnzBase)]
                for elmCmpt in deleteObjsfromCompt:
                    if moose.exists(elmCmpt.path):
                         moose.delete(elmCmpt)
            #deleting compartment 
            for dc in set(set(allCompts) - set(directCompts+indirectCompts)):
                moose.delete(dc)
            
            pruneDanglingObj( kinpath, erSPlist)

Model.argNames = ['modelSource', 'citation', 'citationId', 'authors',
            'modelSubset','readoutMolecules','stimulusMolecules', 'fileName', 'solver', 'notes' ,'scoringFormula','itemstodelete','parameterChange']

#######################################################################

def innerLoad( fd, argNames, dataWidth = 2):
    data = []
    param = []  # list of tuples of objname, field, value.
    arg = {}
    struct = []
    ent = []
    refent = []
    for line in fd:
        cols = line.split( "\t" )
        if len( cols ) == 0 or cols[0] == '' or cols[0].isspace():
            return arg, data, param,struct, ent,refent

        # if keywordMatches( cols[0], 'parameterChange' ):
        #     if len( cols ) >= 4:
        #         param.append( (cols[1], cols[2], float( cols[3] ) ) )
        #     else:
        #         print( "Warning: Model::load parameterChange: need 3 args: entity, field, value. Instead got: '" + line + "'" )
        if keywordMatches( cols[0], 'stimulusMolecules' ):
            ent=cols[1].split(',')
        if keywordMatches( cols[0], 'readoutMolecules' ):
            refent=cols[1].split(',')
        if keywordMatches( cols[0], 'Data' ):
            readData( fd, data, dataWidth ) 
            #print "Ret READ DATA from INNERLOAD", len( data )
            return arg, data, param,struct,ent,refent

        for i in argNames:
            if keywordMatches( cols[0], i ):
                arg[i] = str.strip( nonBlank( cols) )
                continue;
        if keywordMatches(cols[0],"parameterChange"):
            readParameter(fd,param,dataWidth)

        if keywordMatches( cols[0], 'itemstodelete' ):
            struct= cols[1].split(',')

    return arg, data, param, struct, ent, refent

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
                #row.append( float( c ) )
                row.append( ( c ) )
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
    '''
    print " s1 ",s1
    for i in s1:
        print " i .feing ",i, i.className.find('Pool')
        if i.className.find( 'Pool' ) != -1:
            print i.children
            for iis in i:
                f
            if i.className != "Annotator":
                appendees.extend( i.children )
                for j in set( i.children ):
                    if j.className != "Annotator":
                        appendees.extend( j[0].children )
                #print [k.name for k in j[0].children]
    print " appendees ",appendees
    '''
    ret = set( elms + [k[0] for k in appendees] )
    return ret
    #elms.extend( list(set(appendees)) ) # make it unique.
    
def pruneDanglingObj( kinpath, erSPlist):
    erlist = moose.wildcardFind(kinpath+"/##[ISA=Enz],"+kinpath+ "/##[ISA=Reac]")
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
                mWarning = mWarning+"\n"+i.path
                # print (modelWarning +"\n"+i.path)
                # exit()
            elif len(isub) != erSPlist[i]["s"] or len(iprd) != erSPlist[i]["p"]:
                ratelawchanged = True
                mRateLaw = mRateLaw+"\n"+i.path
                # print (modelRateLaw + "\n"+ i.path)
                # exit()

    flist = moose.wildcardFind( kinpath + "/##[ISA=Function]" )
    for i in flist:
        if len(i.neighbors['valueOut']) == 0:
            moose.delete(moose.element(i))
        if len(moose.element(moose.element(i).path+'/x').neighbors['input']) == 0 or  \
            len(moose.element(moose.element(i).path+'/x').neighbors['input']) != i.numVars:
            funcIPchanged = True
            mFunc = mFunc+"\n"+i.path

    if subprdNotfound:
        print (" \nWarning: Found dangling Reaction/Enzyme, model's need to specify this in the itemstodelete for deletion, program will exit now "+mWarning)
    if ratelawchanged:
        print ("\nWarning: This reaction or enzyme's, RateLaw needs correction as it's sub or prd were delete while subsetting, program will exit now"+mRateLaw)
    if funcIPchanged:
        print ("\nWhile subsetting the either one or more input's to the function is missing, this need's to be specified in itemstodelete for deletion, program will exit now"+mFunc)
    if subprdNotfound or ratelawchanged or funcIPchanged:
        exit()

##########################################################################

##########################################################################

def loadTsv( fname ):
    stims = []
    readouts = []
    fs = fname.split('.')
    if len(fs) < 2:
        if fs[-1] != 'tsv':
            print( "Error: file '" + fname + "' should end in .tsv" )
            quit()
    with open( fname ) as fd:
        for line in fd:
            if len( line ) > 1 and line[0] != '#':
                cols = line.split('\t')
                if len( cols ) > 0:
                    if cols[0] == 'Experiment metadata':
                        expt = Experiment.load(fd )
                        print "#########################", cols[0]
                    if cols[0] == 'Stimuli':
                       stims.append( Stimulus.load(fd ) )
                       print "#########################", cols[0]
                    if cols[0] == 'Readouts':
                        readouts.append( Readout.load(fd) )
                        print "#########################", cols[0]
                    if cols[0] == 'Model mapping':
                        model = Model.load(fd )
                        print "#########################", cols[0]
    
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


def main():
    """ This program handles loading a kinetic model, and running it
 with the specified stimuli. The output is then compared with expected output to generate a model score.
    """
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    mfile = 'FindSim_compositeModel_1.g'
    modelWarning = ""
    #mfile = "/home/harsha/genesis_files/gfile/acc90.g"
    if ( len( sys.argv ) < 2 ):
        print( "Usage: " + sys.argv[0] + " file.tsv [modelfile]" )
        quit()
    expt, stims, readouts, model = loadTsv( sys.argv[1] )
    if ( len( sys.argv ) >= 3 ):
        model.fileName = sys.argv[2]
    else:
        model.fileName = mfile
    #This list holds the entire models Reac/Enz sub/prd list for reference
    erSPlist = {}
    # First we load in the model using EE so it is easier to tweak
    if os.path.isfile(model.fileName):
        modelId = moose.loadModel( model.fileName, 'model', 'ee' )
        # moose.delete('/model[0]/kinetics[0]/compartment_1[0]')
        for f in moose.wildcardFind('/model/##[ISA=ReacBase],/model/##[ISA=EnzBase]'):
            erSPlist[f] = {'s':len(f.neighbors['sub']), 'p':len(f.neighbors['prd'])}
        # Then we apply whatever modifications are specified by user or protocol
        moose.Neutral('/model/plots')
        modleWarning = ""
        model.modify( modelId, erSPlist,modelWarning )
        #Then we build the solver.
        buildSolver( modelId, model.solver )

        for i in range( 10, 20 ):
            moose.setClock( i, 0.1 )

        #score, plots = runit( model,stims, readouts )
        # print " ################# "
        #moose.mooseWriteKkit('/model', '/tmp/finalmodel4c.g')

# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
