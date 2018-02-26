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
'''
# Warning: since its looping entire file, some case like citationId in experiment may be empty bcos model's citationId may be empty
# stimuti block is not necessary we can delete entire block or block exist make sure what every empty it doesn't affect the model 
# different type if time-series types at this point no check is make
# check if list items have space between comma
import heapq
import pylab
import numpy
import sys
import moose

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
        print " arg[0] ",arg[0], arg[1], arg[2],arg[3]
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
            timeUnits = 's',
            quantityUnits = 'mM',
            molecules = [],
            field = '',
            settleTime = 300.0, 
            data = []
        ):
        #self.stimulusType = stimulusType
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

    def load( fd ):
        '''
        Model::load builds a model instance from a file and returns it.
        '''
        arg, data, param, struct, ent, refent = innerLoad( fd, Model.argNames )
        model = Model( **arg )
        for i in param:
            model.addParameterChange( i[0], i[1], i[2] )
        for i in struct[:]:
            #model.addStructuralChange( i[0], i[1] )
            model.addStructuralChange(i.lstrip(),"delete")
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
        self.itemstodelete.append((entity,change))
        # if change == 'delete':
        #     self.StructuralChange.append( ( entity, change ) )
        # else:
        #     print( "Warning: Model::addStructuralChange: Unknown modification: " + change )

    def modify( self, modelId ):
        # Start off with things explicitly specified for deletion.
        kinpath = modelId.path
        if self.itemstodelete:
            for ( entity, change ) in self.itemstodelete[:]:
                if moose.exists( kinpath + entity ):
                    obj = moose.element( kinpath + entity )
                    if change == 'delete':
                        moose.delete( obj )
                else:
                    print "Object does not exist ", kinpath+entity
        # Go on to dealing with subsets of model.
        if not( self.modelSubset.lower() == 'all' or self.modelSubset.lower() == 'any' ):
            # Generate list of all included groups
            subsets = self.subset.split( ',')
            directGroups = []
            parentGroups = []
            for i in subsets: # We don't do wildcards here, just enumurate.
                if moose.exists( kinpath + i ):
                    elm = moose.element( kinpath + i )
                    if isGroup( elm ):
                        directGroups.extend( findChildGroups( elm ) )
                    else:
                        parentGroups.append( findParentGroup(elm) )
                else:
                    print("Warning: subset entry '{}' not found".format(i))
            includedGroups = set( directGroups + parentGroups )
            # Generate list of all groups
            allGroups = set( moose.wildcardFind( kinpath + '##[TYPE=Neutral],' + kinpath + '##[ISA=ChemCompt]' ) )
            # Find groups to delete, and delete them.
            excludedGroups = allGroups - includedGroups
            deletees = pruneExcludedElements( excludedGroups )
            for i in deletees:
                moose.delete( i )
            print [i.name for i in moose.wildcardFind( kinpath + '/##[TYPE=Neutral]' )]
            # Generate list of all surviving objects. We're going to get
            # rid of them too, unless they are saved by the subset list.
            survivors = set( moose.wildcardFind( kinpath + '##[0]' ) )
            #print "Survivors = ", sorted([ i.name for i in survivors ])
            # Go through the subsets again in case some are already deleted
            nonGroups = []
            for i in subsets: # We don't do wildcards here, just enumurate.
                if moose.exists( kinpath + i ):
                    elm = moose.element( kinpath + i )
                    if not isGroup( elm ):
                        nonGroups.append( elm )
            nonGroupSet = ornamentPools( nonGroups )
            #print "nonGroups = ", sorted([ i.name for i in nonGroups ])
            deletees = pruneExcludedElements( survivors - nonGroupSet ) - includedGroups
            #print "deletees = ", sorted([ i.name for i in deletees ])
            for i in deletees:
                moose.delete( i )
            pruneDanglingEnzymes( kinpath )
            #print "Whatever is left = ", sorted( [i.name for i in moose.wildcardFind( kinpath + "##" ) ] )

        # Go through and change parameters.
        for (entity, field, value) in self.parameterChange:
            path = kinpath + entity
            if moose.exists( path ):
                moose.element( path ).setField( field, value )
                #print( "Model::modify called with: " + entity + '.' + field  + ' = ' + str( value ) )
            else:
                print( "Warning: Model::modify: object/field not found: " + path + '.' + field )


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
        if keywordMatches( cols[0], 'molecules' ):
            ent=cols[1].split(',')
        
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
                row.append( float( c ) )
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
            print " c "
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
    
    print "expt ", expt.exptSource, expt.citationId, expt.journal, expt.authors
    print " stims ", stims
    for s in stims:
        print " \n stims ",s.timeUnits, s.quantityUnits, s.entity,s.field,s.settleTime, s.data,
    print " readouts ",readouts
    for r in readouts:
        print " \n Readout ",r.readoutType, "TU ", r.timeUnits, "QU ",r.quantityUnits,\
                        " RATIO", r.useRatio, " SUM ",r.useSum, " NO ",r.useNormalization,\
                        "RRT ", r.ratioReferenceTime, "RRD", r.ratioReferenceDose,\
                        "MOL", r.molecules," RRE ", r.ratioReferenceEntity,\
                        "ER ", r.experimentalReadout, "XL ", r.useXlog, "YL ",r.useYlog,\
                        "DATA ",r.data
    print " model ",model
    print " model ",model.modelSource, " \n cit ", model.citation, " \n CITID ",model.citationId, " \nAut ",model.authors, "\n details ",\
                    model.detail, "\n sS ",model.modelSubset,"\n FILE ", model.fileName, " \nsol ",model.solver, "\n n ",\
                    model.notes, " \n pC ",model.parameterChange, " \n SC ",model.itemstodelete
    return expt,stims,readouts,model

def main():
    """ This program handles loading a kinetic model, and running it
 with the specified stimuli. The output is then compared with expected output to generate a model score.
    """
    solver = "gsl"  # Pick any of gsl, gssa, ee..
    mfile = 'acc86.g'
    if ( len( sys.argv ) < 2 ):
        print( "Usage: " + sys.argv[0] + " file.tsv [modelfile]" )
        quit()
    expt = loadTsv( sys.argv[1] )

# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
