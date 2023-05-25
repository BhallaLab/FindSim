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
        # Do other stuff here if we have a param list to compare.
        v1 = np.array( [paramDict[key] for key in sorted(paramDict)] )
        v2 = np.array( [cpd[key] for key in sorted(paramDict)] )
        dp = np.dot( v1, v2 ) / (np.sqrt(v1.dot(v1)) * np.sqrt(v2.dot(v2)) )
        delta = 2*(v1 - v2) / (v1 + v2)
        nrms1 = np.sqrt(np.dot(delta, delta) / len( delta ))
        delta = (v1 - v2) / v1
        nrms2 = np.sqrt(np.dot(delta, delta) / len( delta ))
        print( "nrms1={:.3f},  nrms2={:.3f}  dp={:.3f}".format( 
            nrms1, nrms2, dp ) )


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
        print( "getParamDict has {} entries".format( len( pd ) ) )
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
        moose.element( self.modelId ).name =  "cleared"


class HTScram ( ):
    def __init__( self, scram ):
        self.scram = scram
        self.jsonDict = hillTau.loadHillTau( scram.fname )
        #scaleParam = self.scaleNamedConsts( scaleParam )
        qs = hillTau.getQuantityScale( self.jsonDict )
        hillTau.scaleDict( self.jsonDict, qs )

    def buildModelLookup( self, objMap ):
        # All Mols are keys in modelLookup, plus whatever objMap sets.
        # We ensure that only valid objects are keys.
        for key, val in objMap.items():
            v = val[0]
            self.scram.modelLookup[key] = val

    '''
    def scaleNamedConsts( self, scaleParam ):
        constDict = self.jsonDict.get( "Constants" )
        if constDict:
            newScaleParam = []
            for i in range( 0, len( scaleParam ), 3 ):
                key = scaleParam[i]
                val = scaleParam[i+2]
                if key in constDict:
                    constDict[key] = val
                    #print( "scaling const ", key, " to ", val )
                else:
                    newScaleParam.append( key )
                    newScaleParam.append( scaleParam[i+1] )
                    newScaleParam.append( val )
            # Reassign scaleParam with the found consts removed.
            return newScaleParam
        else:
            return scaleParam
    '''
    def getParamDict( self ):
        pd = {}
        return pd

    def clear( self ):
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
    parser.add_argument( '-s', '--scramble', type = float, help='Optional: Scramble parameters logarithmically over specified range. If range is x, then the parameter is scaled between 1/x to x fold of its original value.' )
    parser.add_argument( '-c', '--compare', type = str, help='Optional: Compare params for two models using NRMS. Argument is comparison file name.' )
    parser.add_argument( '-o', '--outputModel', type = str, help='Optional: File name for output model to save with scrambled parameters.' )

    args = parser.parse_args()

    scram = Scram( args.model, args.map )

    if args.allParams:
        pd = scram.getParamDict()

    if args.scramble and args.scramble > 0:
        scram.scramble( pd, args.scramble )

    if args.outputModel:
        scram.dumpModel( args.outputModel )

    if args.compare:
        scram.compare( args.compare, args.map, pd )

# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
