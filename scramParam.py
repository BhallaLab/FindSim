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
            field = field[1:]
            if field == "concInit":
                pd[key] = self.model.molInfo[obj].concInit
            else:
                ri = self.model.reacInfo[obj]
                pd[key] = getattr( self.model.reacInfo[obj], field, 0.0 )
    
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

def matchParamByName( path, name ):
    '''
    Looks for a match of the specified object name in a full object path.
    Returns True if there is a match.

    The typical Moose object path is something like 
        /model[0]/kinetics[0]/EGFR[0]/EGFR[0]. 
    Suppose we wanted to match EGFR. We want it to look up the final part 
    of the string, ignoring all the earlier portions, and stripping out the
    [0]. 
    Here is a problematic (but common) case. Suppose we wanted the enzyme 
    site on PKC: 
        /model[0]/kinetics[0]/PKC[0]/PKC[0]/enz
    But there is also an enzyme site on PKA.
        /model[0]/kinetics[0]/PKA[0]/PKA[0]/enz
    To disambiguate, we permit specification by longer strings with the "/"
    separators, such as "PKC/enz"
    In the case of HillTau the naming is simpler and all molecules and 
    reactions have a unique name.
    '''
    if len( path.split(".") ) > 1: # It has fields
        pField = path.split(".")[-1]
        nField = name.split(".")[-1]
        if pField != nField:
            return False
        path = path[:-len(pField)-1]
        name = name[:-len(pField)-1]

    spPath = path.split( "/" )
    spName = name.split( "/" )
    if len( spName ) > len( spPath ):
        return False
    for ii, nn in enumerate( reversed(spName ) ):
        p = spPath[-ii - 1]
        pp = p[:-3] if p[-3:] == "[0]" else p
        if pp != nn:
            return False
    return True




def main():
    """ This program accesses parameters of SBML or HillTau models to scramble them.
    """
    parser = argparse.ArgumentParser( description = 'scramParam argument parser.\n'
    'This program loads a kinetic model, and compares or scrambles the parameters\n')

    parser.add_argument( 'model', type = str, help='Required: filename of model, which can be SBML, .g or HillTau.')
    parser.add_argument( 'map', type = str, help='Required: mapping file from shortcut names to sim-specific strings. JSON format.' )
    parser.add_argument( '-p', '--paramList', type = str, nargs = '+', help='Optional: Parameters specified as obj.field [obj.field obj.field...]' )
    parser.add_argument( '-a', '--allParams', action="store_true", help='Flag: Operate on all nonzero parameters in model' )
    parser.add_argument( '-f', '--freezeParams', type = str, nargs = '+', help='Optional: Freeze (do not vary) the listed parameters even if they turn up in the -p or -a arguments. Parameters specified as obj.field [obj.field obj.field...]' )
    parser.add_argument( '-l', '--listParams', action="store_true", help='Flag: Count and print out number of nonzero parameters in model' )
    parser.add_argument( '-s', '--scramble', type = float, help='Optional: Scramble parameters logarithmically over normal distrib with specified range. The width of the normal distribution is the log of the specified range.' )
    parser.add_argument( '-ls', '--logLinScramble', type = float, help='Optional: Scramble parameters logarithmically over specified range. If range is x, then the parameter is scaled between 1/x to x fold of its original value.' )
    parser.add_argument( '-o', '--outputModel', type = str, help='Optional: File name for output model to save with scrambled parameters.' )
    parser.add_argument( '-n', '--numOutputModels', type = int, help='Optional: number of scrambled models to generate. Default = 1.', default = 1 )

    args = parser.parse_args()

    scram = Scram( args.model, args.map )

    if args.allParams:
        pd = scram.getParamDict()

    if args.freezeParams:
        for ff in args.freezeParams:
            popped = False
            for pp in pd:
                if matchParamByName( pp, ff ):
                    pd.pop( pp )
                    popped = True
                    break;
            if not popped:
                print( "Warning: freezeParams did not find: ", ff )

    if args.listParams:
        pd = scram.getParamDict()
        print( "Number of non-zero parameters = ", len( pd ) )
        for ii, key in enumerate( sorted( pd ) ):
            print( "{:<4d}{:65s} {:.3g}".format( ii+1, key, pd[key] ) )
        quit()

    origParamDict = dict( pd ) # Make the reference copy.
    if args.outputModel:
        fname, fext = os.path.splitext( args.outputModel )
    else:
        fname, fext = os.path.splitext( args.model )
        fname = "o_" + fname

    for idx in range( args.numOutputModels ):
        pd = dict( origParamDict ) # Restore to orig params
        if args.logLinScramble and args.logLinScramble > 0:
            scram.logLinScramble( pd, args.logLinScramble )
        elif args.scramble and args.scramble > 0:
            scram.normScramble( pd, args.scramble )
        else:
            print( "Error: Must specify either scramble or logLinScramble options" )
            quit()

        if args.numOutputModels == 1:
            scram.dumpModel( "{}{}".format( fname, fext ) )
        else:
            scram.dumpModel( "{}_{:03d}{}".format( fname, idx, fext ) )

# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
