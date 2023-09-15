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
 * File:            scramParam.py
 * Description:     Utility to scramble model parameters
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 *  Copyright (c) U.S. Bhalla 2023
 ********************************************************************/
 '''

import os
import argparse
import numpy as np
import json
import moose
import hillTau
import sys

def fsig( x ):
    # Format floats to 4 sig fig for cleaner files
    return float( "{:.4g}".format(x) )

class Scram:
    def __init__( self, fname ):
        self.fname = fname
        fileName, file_extension = os.path.splitext( fname )
        self.file_extension = file_extension
        if file_extension in [".xml", ".sbml", ".g"]:
            self.model = MooseScram( self )
        elif file_extension == ".json":
            self.model = HTScram( self )
        else:
            print( "Error, model has to be either SBML (.xml) or HillTau (.json)" )

    def getParamDict( self, includeZero = False ):
        return self.model.getParamDict( includeZero )

    def fillParamDict( self, pd ):
        return self.model.fillParamDict( pd )

    def setParamDict( self, paramDict ):
        self.model.setParamDict( paramDict )

    def dumpModel( self, dumpFname ):
        self.model.dumpModel( dumpFname )

    def logLinScramble( self, paramDict, scrambleRange ):
        log = np.log( scrambleRange )
        for key, val in paramDict.items():
            paramDict[key] = np.exp( np.log( val ) + np.random.uniform(-log, log) )
        self.model.setParamDict( paramDict )

    def normScramble( self, paramDict, scrambleRange ):
        log = np.log( scrambleRange )
        for key, val in paramDict.items():
            paramDict[key] = np.exp( np.log( val ) + np.random.normal(0.0, log) )
        self.model.setParamDict( paramDict )
    def findObjPath( self, uname, noRaise = False ):
        return self.model.findObjPath( uname, noRaise )

    def clear( self):
        self.model.clear()


class MooseScram ():
    def __init__( self, scram ):
        self.scram = scram
        if scram.file_extension == '.xml':
            self.modelId, errormsg = moose.readSBML( scram.fname, 'model', 'ee' )
        elif scram.file_extension == '.g':
            self.modelId = moose.loadModel( scram.fname, 'model', 'ee' )
        self.kinPath = self.modelId.path + "/kinetics"

    def findObjPath( self, uname, noRaise = False ):
        '''
        Model:: findObjPath locates objects uniquely specified by a string. 
        The object can be located at any depth in the model tree.
        The identifier string typically consists of the name of an object,
        but it may be necessary to disambiguate it by including its parent
        name as well.
        For example, if there is a foo/bar and a zod/bar, then we will 
        have to pass "zod/bar" to uniquely specify the object.
        '''
        #name = uname.encode( 'ascii' )
        parentLen = len( self.modelId.path + "/kinetics[0]" )
        name = uname
        rootpath = self.modelId.path
        try1 = moose.wildcardFind( rootpath+'/' + name )
        try2 = moose.wildcardFind( rootpath+'/##/' + name )
        try2 = [ i for i in try2 if not '/model[0]/plots[0]' in i.path ]  
        if len( try1 ) + len( try2 ) > 1:
            raise NameError( "findObj: ambiguous name: '{}'".format(name) )
        if len( try1 ) + len( try2 ) == 0:
            if noRaise:
                return '/'
            else:
                print( "findObj: No object found on '{}' named: '{}'".format( rootpath, name) )
                quit()
        if len( try1 ) == 1:
            #print( "TRY1 = ", try1[0].path )
            return try1[0].path[parentLen:].replace( "[0]", "" )
        else:
            #print( "TRY2 = ", try2[0].path )
            return try2[0].path[parentLen:].replace( "[0]", "" )

    def getParamDict( self, includeZero = False ):
        """
        Returns dict of {objectPath.field : value} for all params in model.
        It leaves out parameters with value zero unless includeZero is True.
        """
        pd = {}
        pools = moose.wildcardFind( self.modelId.path +'/##[ISA=PoolBase]' )
        enzs = moose.wildcardFind( self.modelId.path +'/##[ISA=EnzBase]' )
        reacs = moose.wildcardFind( self.modelId.path +'/##[ISA=Reac]' )
        parentLen = len( self.modelId.path + "/kinetics[0]" )
        #print( "self.modelId.path", self.modelId.path, self.kinPath )
        for pp in pools:
            ppath = pp.path[parentLen:].replace( "[0]", "" )
            if includeZero or pp.concInit > 0.0:
                pd[ppath + ".concInit"] = pp.concInit
        for ee in enzs:
            epath = ee.path[ parentLen: ].replace( "[0]", "")
            pd[epath + ".kcat"] = ee.kcat
            pd[epath + ".Km"] = ee.Km
        for rr in reacs:
            rpath = rr.path[ parentLen: ].replace( "[0]", "")
            if includeZero or rr.Kb > 0:
                pd[rpath + ".Kb"] = rr.Kb
            if includeZero or rr.Kf > 0:
                pd[rpath + ".Kf"] = rr.Kf
        #print( "getParamDict has {} entries".format( len( pd ) ) )
        return pd

    def fillParamDict( self, paramList ):
        """
        Returns dict of {objectPath.field : value} for listedParams.
        """
        pd = {}
        for key in paramList:
            obj, field = os.path.splitext( key )
            #print( "FILLPA", self.kinPath, obj, field )
            pd[key] = moose.element( self.kinPath + obj ).getField( field[1:] )
        return pd
    
    def setParamDict( self, pd ):
        for key, val in pd.items():
            obj, field = os.path.splitext( key )
            #print( "Set Param Dict:   ", self.kinPath + obj, field, val )
            moose.element( self.kinPath + obj ).setField( field[1:], val )

    def dumpModel( self, dumpFname ):
        if len(dumpFname) > 2:
            if dumpFname[-2:] == '.g':
                moose.writeKkit( self.modelId.path, dumpFname )
            elif len(dumpFname) > 4 and dumpFname[-4:] == '.xml':
                moose.writeSBML( self.modelId.path, dumpFname )
            else:
                print( "Moose Model type not known: '{}'".format(dumpFname))
                quit()
                
    def clear( self ):
        #print( self.modelId, self.modelId.path )
        if self.modelId and moose.exists( self.modelId.path ):
            moose.delete( self.modelId )
            self.modelId = None
        #moose.element( self.modelId ).name =  "cleared"


class HTScram ( ):
    def __init__( self, scram ):
        self.scram = scram
        self.jsonDict = hillTau.loadHillTau( scram.fname )
        self.qs = hillTau.getQuantityScale( self.jsonDict )
        hillTau.scaleDict( self.jsonDict, self.qs )
        self.model = hillTau.parseModel( self.jsonDict )
        self.onlyTau = {}   # a dict of name:flag to specify it tau==tau2

    def fillParamDict( self, paramList ):
        pd = {}
        for key in paramList:
            obj, field = os.path.splitext( key )
            field = field[1:]
            if field == "concInit":
                pd[key] = self.model.molInfo[obj].concInit
            else:
                ri = self.model.reacInfo[obj]
                pd[key] = getattr( self.model.reacInfo[obj], field, 0.0 )
        return pd
    
    def setParamDict( self, pd ):
        for key, val in pd.items():
            obj, field = os.path.splitext( key )
            field = field[1:]
            #print( "setParam {}.{} to {}".format( obj, field, val ) )
            if field == "concInit":
                self.model.molInfo[obj].concInit = val
            else:
                setattr( self.model.reacInfo[obj], field, val )
                if (field == "tau") and self.onlyTau[obj]: #Same tau2
                    self.model.reacInfo[obj].tau2 = val

    def ht2dict( self ):
        for key, val in self.model.molInfo.items():
            if val.concInit > 0.0:
               self.jsonDict["Groups"][val.grp]["Species"][val.name] = fsig( val.concInit )
        for key, val in self.model.reacInfo.items():
            rr = self.jsonDict["Groups"][val.grp]["Reacs"][val.name]
            rr["KA"] = fsig( val.KA )
            rr["tau"] = fsig( val.tau )
            if fsig( val.tau ) != fsig( val.tau2 ):
                rr[ "tau2" ] = fsig( val.tau2 )
            if val.baseline > 0.0:
                rr[ "baseline" ] = fsig( val.baseline )
            if val.gain != 1.0:
                rr[ "gain" ] = fsig( val.gain )
            if (len(val.subs ) > 2) and (val.subs[-1] != val.subs[1]):
                rr[ "Kmod" ] = fsig( val.Kmod )
                rr[ "Amod" ] = fsig( val.Amod )

    def dumpModel( self, dumpFname ):
        if len(dumpFname) > 2:
            f, extn = os.path.splitext( dumpFname )
            if extn == '.json':
                self.ht2dict()
                hillTau.scaleDict( self.jsonDict, 1.0 / self.qs )

                with open( dumpFname, 'w') as f:
                    json.dump( self.jsonDict, f, indent = 4)
            else:
                print("HillTau file type not known: '{}'".format(dumpFname))
                quit()


    def getParamDict( self, includeZero = False ):
        pd = {}
        for key, val in self.model.molInfo.items():
            rr = self.model.reacInfo.get( key )
            if (includeZero or val.concInit > 0.0) and not( rr ):
                pd[ key + ".concInit" ] = val.concInit
            if rr:
                if rr.isBuffered:
                    pd[ key + ".concInit" ] = val.concInit
                    continue
                pd[ key + ".KA" ] = rr.KA
                pd[ key + ".tau" ] = rr.tau
                if rr.tau != rr.tau2:
                    pd[ key + ".tau2" ] = rr.tau2
                    self.onlyTau[key] = False
                else:
                    self.onlyTau[key] = True
                if includeZero or rr.baseline > 0.0:
                    pd[ key + ".baseline" ] = rr.baseline
                if rr.gain != 1.0:
                    pd[ key + ".gain" ] = rr.gain
                if (len(rr.subs ) > 2) and (rr.subs[-1] != rr.subs[1]):
                    pd[ key + ".Kmod" ] = rr.Kmod
                    pd[ key + ".Amod" ] = rr.Amod
        return pd

    def findObjPath( self, uname, noRaise = False ):
        return uname

    def clear( self ):
        # deleting the Python object will clear it.
        return

def lookupParamList( mapFile, paramList, scram ):
    """ Returns list of params using sim-specific path.field format.
    Also opens and returns mapFile as a dict.
    If paramList is None, then returns all params.
    """
    if not mapFile:
        return paramList, None
    if mapFile.split('.')[-1] != 'json':
        raise ImportError( "Map file '{}' not in JSON format".format(mapFile) )
    try: 
        with open( mapFile ) as json_file:
            m1 = json.load( json_file )
            m2 = {}
            for key, val in m1.items():
                #print("key = ", key, " val = ", val )
                objPath = scram.findObjPath( str( val[0] ) )
                #print("objPath  = ", objPath )
                m2[ str(key) ] = objPath
            if not paramList:   # return all params
                return list(scram.getParamDict()), m2
            ret = lookupListFromMap( m2, paramList )
            # print( "M2 = ", m2 )
            return ret, m2
    except FileNotFoundError:
        print( "Map file '{}' not found".format(mapFile) )
        quit()
        #raise ImportError( "Map file '{}' not found".format(mapFile) )
    except Exception as e:
        print( "Some other error: ", e)
        quit()

def lookupListFromMap( mapDict, paramList ):
    ret = []
    for pp in paramList:
        objName, field = os.path.splitext( pp )
        mm = mapDict.get( objName )
        if mm:
            ret.append( mm + field )
    return ret


def generateScrambled( inputModel, mapFile, outputModel, numOutputModels, paramList, scramRange, isLogNorm = True, freezeParams = None ):

    scram = Scram( inputModel )

    # paramDict has {key = obj.field: value = value}
    innerParamList, mapDict = lookupParamList( mapFile, paramList, scram )
    #print( "NUM PARAMS = ", len( innerParamList ), len( mapDict ) )

    # Drop those in freezeParams if specified.
    if freezeParams:
        innerFreezeParams = lookupListFromMap( mapDict, freezeParams )
        #print( mapDict )
        #print( innerFreezeParams )
        for ff in innerFreezeParams:
            #print( "FFFFFFFFFFFF ",  ff )
            if ff in innerParamList:
                innerParamList.remove( ff )
            else:
                print( "Warning: freezeParams did not find: ", ff )

    #print( innerParamList )
    origParamDict = scram.fillParamDict( innerParamList ) # Reference copy.
    #print( origParamDict )
    if outputModel:
        fname, fext = os.path.splitext( outputModel )
    else:
        fname, fext = os.path.splitext( inputModel )
        fname = "o_" + fname

    for idx in range( numOutputModels ):
        pd = dict( origParamDict ) # Restore to orig params
        if isLogNorm:
            scram.normScramble( pd, scramRange )
        else:
            scram.logLinScramble( pd, scramRange )

        if numOutputModels == 1:
            scram.dumpModel( "{}{}".format( fname, fext ) )
        else:
            scram.dumpModel( "{}_{:03d}{}".format( fname, idx, fext ) )

def mergeModels( inputModel, mapFile, insertModel, outputModel, paramList ):
    scram2 = Scram( insertModel )
    innerParamList, mapDict = lookupParamList( mapFile, paramList, scram2 )
    #pd2 = { pp:0.0 for pp in innerParamList }
    pd2 = scram2.fillParamDict( innerParamList )
    scram2.model.clear()

    scram1 = Scram( inputModel )
    pd1 = scram1.getParamDict()   # Get all parameters
    # Now replace params with those from pd2
    scram1.setParamDict( pd2 )
    scram1.dumpModel( "{}".format( outputModel ) )
    scram1.model.clear()

def main():
    """ This program accesses parameters of SBML or HillTau models to scramble them.
    """
    parser = argparse.ArgumentParser( description = 'This program loads a kinetic model, and compares or scrambles the parameters. By default it looks at all non-zero parameters.\n')

    parser.add_argument( 'model', type = str, help='Required: filename of model, which can be SBML, .g or HillTau.')
    parser.add_argument( '-map', "--map", type = str, help='Optional: filename of mapfile, which is a json file. If not specified it assumes that the parameters directly look up internal model definitions.')
    parser.add_argument( '-p', '--paramList', type = str, nargs = '+', help='Optional: Restrict scramble parameters to those specified as obj.field [obj.field obj.field...]. Default: use all parameters.' )
    parser.add_argument( '-f', '--freezeParams', type = str, nargs = '+', help='Optional: Remove listed parameters from set to scramble. Params defined ase obj.field [obj.field obj.field...]' )
    parser.add_argument( '-s', '--scramble', type = float, help='Optional: Scramble parameters logarithmically over normal distrib with specified range. The width of the normal distribution is the log of the specified range.' )
    parser.add_argument( '-ls', '--logLinScramble', type = float, help='Optional: Scramble parameters logarithmically over specified range. If range is x, then the parameter is scaled between 1/x to x fold of its original value.' )
    parser.add_argument( '-o', '--outputModel', type = str, help='Optional: File name for output model to save with scrambled parameters. If not specified, it uses the input model file name with the prefix "o_". If there are multiple output files it indexes them with a suffix "_N" where N is a 3-digit number, zero padded on the left, such as "_015."' )
    parser.add_argument( '-i', '--insertModel', type = str, help='Optional: File name for insert model whose parameters have to be inserted (merged) into the first model. Only the parameters in the paramList are inserted. If this option is used then no scrambling is done, hence -n, -s, and -ls options are ignored.' )
    parser.add_argument( '-n', '--numOutputModels', type = int, help='Optional: number of scrambled models to generate. Default = 1.', default = 1 )

    args = parser.parse_args()

    if args.insertModel:
        if not (args.paramList and args.outputModel):
            print( "Error: to insert a model we need the paramList of params to insert, and the outputModel into which the merged model should be saved." )
            quit()
        mergeModels( args.model, args.map, args.insertModel, 
            args.outputModel, args.paramList )
        quit()

    if args.scramble:
        scramRange = args.scramble
        isLogNorm = True
    elif args.logLinScramble:
        scramRange = args.logLinScramble
        isLogNorm = False
    else:
        print( "Error: must define scramble range either through 'scramble' or through 'logLinScramble' keywords" )
        quit()

    generateScrambled( args.model, args.map, args.outputModel, 
            args.numOutputModels, args.paramList, scramRange, 
            isLogNorm, args.freezeParams )


# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()

