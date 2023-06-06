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
import random

def fsig( x ):
    # Format floats to 4 sig fig for cleaner files
    return float( "{:.4g}".format(x) )

class Scram:
    def __init__( self, fname, mapfname ):
        self.fname = fname
        self.mapfname = mapfname
        self.modelLookup = {}
        fileName, file_extension = os.path.splitext( fname )
        self.file_extension = file_extension
        if file_extension in [".xml", ".sbml", ".g"]:
            self.model = MooseScram( self )
        elif file_extension == ".json":
            self.model = HTScram( self )
        else:
            print( "Error, model has to be either SBML (.xml) or HillTau (.json)" )

        with open( mapfname ) as fd:
            self.objMap = json.load( fd )
        self.model.buildModelLookup( self.objMap )

    def getParamDict( self ):
        return self.model.getParamDict()

    def fillParamDict( self, pd ):
        self.model.fillParamDict( pd )

    def setParamDict( self, paramDict ):
        self.model.setParamDict( paramDict )

    def dumpModel( self, dumpFname ):
        self.model.dumpModel( dumpFname )

    def scramble( self, paramDict, scrambleRange ):
        log = np.log( scrambleRange )
        for key, val in paramDict.items():
            paramDict[key] = np.exp( np.log( val ) + random.uniform(-log, log) )
        self.model.setParamDict( paramDict )


    def compare( self, cmpModel, mapFile, paramDict ):
        self.model.clear()
        cmp = Scram( cmpModel, mapFile )
        cpd = dict( paramDict )
        cmp.fillParamDict( cpd )
        cmp.model.clear()
        # Do other stuff here if we have a param list to compare.
        v1 = np.array( [paramDict[key] for key in sorted(paramDict)] )
        v2 = np.array( [cpd[key] for key in sorted(paramDict)] )
        dp = np.dot( v1, v2 ) / (np.sqrt(v1.dot(v1)) * np.sqrt(v2.dot(v2)) )
        delta = 2*(v1 - v2) / (v1 + v2)
        nrms1 = np.sqrt(np.dot(delta, delta) / len( delta ))
        delta = (v1 - v2) / v1
        nrms2 = np.sqrt(np.dot(delta, delta) / len( delta ))
        return nrms1, nrms2, dp


class MooseScram ():
    def __init__( self, scram ):
        self.scram = scram
        if scram.file_extension == '.xml':
            self.modelId, errormsg = moose.readSBML( scram.fname, 'model', 'ee' )
        elif scram.file_extension == '.g':
            self.modelId = moose.loadModel( scram.fname, 'model', 'ee' )

    def buildModelLookup( self, objMap ):
        for key, paths in objMap.items():
            foundObj = [ self.findObj( p, noRaise = True ) for p in paths ]
            foundObj = [ j.path for j in foundObj if j.name != '/' ]
            if len( foundObj ) > 0:
                self.scram.modelLookup[key] = foundObj

    def findObj( self, uname, noRaise = False ):
        '''
        Model:: findObj locates objects uniquely specified by a string. 
        The object can be located at any depth in the model tree.
        The identifier string typically consists of the name of an object,
        but it may be necessary to disambiguate it by including its parent
        name as well.
        For example, if there is a foo/bar and a zod/bar, then we will 
        have to pass "zod/bar" to uniquely specify the object.
        '''
        #name = uname.encode( 'ascii' )
        name = uname
        rootpath = self.modelId.path
        try1 = moose.wildcardFind( rootpath+'/' + name )
        try2 = moose.wildcardFind( rootpath+'/##/' + name )
        try2 = [ i for i in try2 if not '/model[0]/plots[0]' in i.path ]  
        if len( try1 ) + len( try2 ) > 1:
            raise SimError( "findObj: ambiguous name: '{}'".format(name) )
        if len( try1 ) + len( try2 ) == 0:
            if noRaise:
                return moose.element('/')
            else:
                print( "findObj: No object found on '{}' named: '{}'".format( rootpath, name) )
                quit()
        if len( try1 ) == 1:
            return try1[0]
        else:
            return try2[0]

    def getParamDict( self ):
        pd = {}
        pools = moose.wildcardFind( self.modelId.path +'/##[ISA=PoolBase]' )
        enzs = moose.wildcardFind( self.modelId.path +'/##[ISA=EnzBase]' )
        reacs = moose.wildcardFind( self.modelId.path +'/##[ISA=Reac]' )
        for pp in pools:
            if pp.concInit > 0.0:
                pd[pp.path + ".concInit"] = pp.concInit
        for ee in enzs:
            pd[ee.path + ".kcat"] = ee.kcat
            pd[ee.path + ".Km"] = ee.Km
        for rr in reacs:
            if rr.Kb > 0:
                pd[rr.path + ".Kb"] = rr.Kb
            if rr.Kf > 0:
                pd[rr.path + ".Kf"] = rr.Kf
        #print( "getParamDict has {} entries".format( len( pd ) ) )
        return pd

    def fillParamDict( self, pd ):
        for key in pd:
            obj, field = os.path.splitext( key )
            pd[key] = moose.element( obj ).getField( field[1:] )
    
    def setParamDict( self, pd ):
        for key, val in pd.items():
            obj, field = os.path.splitext( key )
            moose.element( obj ).setField( field[1:], val )

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
        #scaleParam = self.scaleNamedConsts( scaleParam )
        self.qs = hillTau.getQuantityScale( self.jsonDict )
        hillTau.scaleDict( self.jsonDict, self.qs )
        #self.extendObjMap( ) # This is in simWrapHillTau
        # and adds entries into the ObjMap if not already there
        #self.buildModelLookup( self.objMap) # Called by parent Scram class
        self.model = hillTau.parseModel( self.jsonDict )
        self.onlyTau = {}   # a dict of name:flag to specify it tau==tau2

    def buildModelLookup( self, objMap ):
        # All Mols are keys in modelLookup, plus whatever objMap sets.
        # We ensure that only valid objects are keys.
        for key, val in objMap.items():
            v = val[0]
            self.scram.modelLookup[key] = val


    def fillParamDict( self, pd ):
        for key in pd:
            obj, field = os.path.splitext( key )
            if field == "concInit":
                pd[key] = self.model.molInfo[obj].concInit
            else:
                ri = self.model.reacInfo[obj]
                pd[key] = getattr( self.model.reacInfo[obj], field, 0.0 )
    
    def setParamDict( self, pd ):
        for key, val in pd.items():
            obj, field = os.path.splitext( key )
            field = field[1:]
            print( "setParam {}.{} to {}".format( obj, field, val ) )
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


    def getParamDict( self ):
        pd = {}
        for key, val in self.model.molInfo.items():
            rr = self.model.reacInfo.get( key )
            if (val.concInit > 0.0) and not( rr ):
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
                if rr.baseline > 0.0:
                    pd[ key + ".baseline" ] = rr.baseline
                if rr.gain != 1.0:
                    pd[ key + ".gain" ] = rr.gain
                if (len(rr.subs ) > 2) and (rr.subs[-1] != rr.subs[1]):
                    pd[ key + ".Kmod" ] = rr.Kmod
                    pd[ key + ".Amod" ] = rr.Amod
        return pd

    def clear( self ):
        # deleting the Python object will clear it.
        return


def main():
    """ This program accesses parameters of SBML or HillTau models to scramble them, compare them, or otherwise manipulate them.
    """
    parser = argparse.ArgumentParser( description = 'scramParam argument parser.\n'
    'This program loads a kinetic model, and compares or scrambles the parameters\n')

    parser.add_argument( 'model', type = str, help='Required: filename of model, which can be SBML, .g or HillTau.')
    parser.add_argument( 'map', type = str, help='Required: mapping file from shortcut names to sim-specific strings. JSON format.' )
    parser.add_argument( '-p', '--paramList', type = str, nargs = '+', help='Optional: Parameters specified as obj.field [obj.field obj.field...]' )
    parser.add_argument( '-a', '--allParams', action="store_true", help='Flag: Operate on all nonzero parameters in model' )
    parser.add_argument( '-f', '--freezeParams', type = str, nargs = '+', help='Optional: Freeze (do not vary) the listed parameters even if they turn up in the -p or -a arguments. Parameters specified as obj.field [obj.field obj.field...]' )
    parser.add_argument( '-l', '--listParams', action="store_true", help='Flag: Count and print out number of nonzero parameters in model' )
    parser.add_argument( '-s', '--scramble', type = float, help='Optional: Scramble parameters logarithmically over specified range. If range is x, then the parameter is scaled between 1/x to x fold of its original value.' )
    parser.add_argument( '-c', '--compare', type = str, help='Optional: Compare params for two models using NRMS. Argument is comparison file name.' )
    parser.add_argument( '-o', '--outputModel', type = str, help='Optional: File name for output model to save with scrambled parameters.' )

    args = parser.parse_args()

    scram = Scram( args.model, args.map )

    if args.allParams:
        pd = scram.getParamDict()

    if args.freezeParams:
        for ff in args.freezeParams:
            if pd.get( ff ):
                pd.pop( ff )
            else:
                print( "Warning: freezeParams did not find: ", ff )

    if args.listParams:
        pd = scram.getParamDict()
        print( "Number of non-zero parameters = ", len( pd ) )
        for ii, key in enumerate( sorted( pd ) ):
            print( "{:<4d}{:65s} {:.3g}".format( ii+1, key, pd[key] ) )
        quit()


    if args.scramble and args.scramble > 0:
        scram.scramble( pd, args.scramble )

    if args.outputModel:
        scram.dumpModel( args.outputModel )

    if args.compare:
        nrms1, nrms2, dp = scram.compare( args.compare, args.map, pd )
        print( "nrms1={:.3f},  nrms2={:.3f}  dp={:.3f}".format( 
            nrms1, nrms2, dp ) )

# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
