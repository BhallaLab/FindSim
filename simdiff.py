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
 * File:            simdiff.py
 * Description:     Utility to compare model entities and parameters
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
import math
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
            print( "Error, model has to be either SBML (.xml), kkit (.g) or HillTau (.json)" )

        with open( mapfname ) as fd:
            self.objMap = json.load( fd )
        self.model.buildModelLookup( self.objMap )

    def getParamDict( self ):
        return self.model.getParamDict()

    def fillParamDict( self, pd ):
        self.model.fillParamDict( pd )

    def compare( self, pd1, pd2 ):
        matchKeys = sorted( key for key in pd1 if key in pd2 )
        v1 = np.array( [pd1[key] for key in matchKeys ] )
        v2 = np.array( [pd2[key] for key in matchKeys ] )
        dp = np.dot( v1, v2 ) / (np.sqrt(v1.dot(v1)) * np.sqrt(v2.dot(v2)) )
        delta = 2*(v1 - v2) / (v1 + v2)
        nrms1 = np.sqrt(np.dot(delta, delta) / len( delta ))
        delta = (v1 - v2) / v1
        nrms2 = np.sqrt(np.dot(delta, delta) / len( delta ))
        return nrms1, nrms2, 1.0 - dp

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
        objSet = set(())
        pools = moose.wildcardFind( self.modelId.path +'/##[ISA=PoolBase]' )
        enzs = moose.wildcardFind( self.modelId.path +'/##[ISA=EnzBase]' )
        reacs = moose.wildcardFind( self.modelId.path +'/##[ISA=Reac]' )
        parentLen = len( self.modelId.path + "/kinetics[0]" )
        for pp in pools:
            ppath = pp.path[parentLen:].replace( "[0]", "" )
            if pp.concInit > 0.0:
                pd[ppath + ".concInit"] = pp.concInit
            objSet.add( ppath )
        for ee in enzs:
            epath = ee.path[ parentLen: ].replace( "[0]", "")
            pd[epath + ".kcat"] = ee.kcat
            pd[epath + ".Km"] = ee.Km
            objSet.add( epath )
        for rr in reacs:
            rpath = rr.path[ parentLen: ].replace( "[0]", "")
            if rr.Kb > 0:
                pd[rpath + ".Kb"] = rr.Kb
            if rr.Kf > 0:
                pd[rpath + ".Kf"] = rr.Kf
            objSet.add( rpath )
        #print( "getParamDict has {} entries".format( len( pd ) ) )
        return pd, objSet

    def fillParamDict( self, pd ):
        for key in pd:
            obj, field = os.path.splitext( key )
            pd[key] = moose.element( obj ).getField( field[1:] )
                
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

    def getParamDict( self ):
        pd = {}
        objSet = set(())
        for key, val in self.model.molInfo.items():
            objSet.add( key )
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
        return pd, objSet

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
    """ This program compares ODE or HillTau models.
    """
    parser = argparse.ArgumentParser( description = 'simdiff argument parser.\n'
    'This program loads two kinetic models, and compares them for presence of entities and for values of parameters\n')

    parser.add_argument( 'model', type = str, help='Required: filename of first model, which can be SBML, .g or HillTau.')
    parser.add_argument( 'map', type = str, help='Required: mapping file from shortcut names to sim-specific strings. JSON format.' )
    parser.add_argument( 'model2', type = str, help='Required: filename of second model, which can be SBML, .g or HillTau.')
    parser.add_argument( '-map2', '--map2', type = str, help='Optional: mapping file for second model. JSON format. Default is to use same map file for both models' )
    parser.add_argument( '-lp', '--listParams', action="store_true", help='Flag: Count and print out number of nonzero parameters in model' )

    args = parser.parse_args()

    scram = Scram( args.model, args.map )
    pd1, os1 = scram.getParamDict()
    scram.model.clear()

    if args.listParams:
        print( "Number of non-zero parameters = ", len( pd1 ) )
        for ii, key in enumerate( sorted( pd1 ) ):
            print( "{:<4d}{:65s} {:.3g}".format( ii+1, key, pd1[key] ) )
        quit()


    map2 = args.map2 if args.map2 else args.map

    scram2 = Scram( args.model2, map2 )
    pd2, os2 = scram2.getParamDict()
    scram2.model.clear()

    diff = os1.difference(os2)
    end = "None\n" if len( diff ) == 0 else "\n"
    print( "Objects present in first but not second model:", end = end )
    for ii, dd in enumerate( diff ):
        print( ii, dd )

    diff = os2.difference(os1)
    end = "None\n" if len( diff ) == 0 else "\n"
    print( "Objects present in second but not first model:", end = end )
    for ii, dd in enumerate( diff ):
        print( ii, dd )

    # At present this does not handle cases where one HT model has an
    # optional param such as baseline, and the other does not.

    print( "Comparison between parameters:" )
    numDiff = 0
    for pp, vv in pd1.items():
        vv2 = pd2.get( pp )
        if vv2 and ( not math.isclose( vv, vv2 ) ):
            numDiff += 1
            print( "{:<4d}{:49s}{:<13.4g}{:<13.4g}".format( numDiff, pp, vv, vv2 ) )
    if numDiff == 0:
        print( "    No differences found between parameters." )

        
    print( "RMS and dot product distances between models:" )
    nrms1, nrms2, dp = scram.compare( pd1, pd2 )
    print( "nrms1={:8.3f}     nrms2={:8.3f}     dp={:8.3f}".format( 
            nrms1, nrms2, dp ) )

# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
