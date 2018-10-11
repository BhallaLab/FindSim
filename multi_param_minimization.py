
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

'''
*******************************************************************
 * File:            Brent_minimization.py
 * Description:
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/

/**********************************************************************
** This program is part of 'FindSim', the
** Framework for Integrating Neuronal Data and SIgnaling Models
**           copyright (C) 2003-2018 Upinder S. Bhalla. and NCBS
**********************************************************************/

This script does a one-dimensional minimization on the model. It runs the 
findSim program on all tsv files in the specified directory with 
modifications of the selected parameters. It computes the weighted score 
for each run as the return value for the minimization function. While the
Brent algorithm is serial, there are lots of indvidual tsv calculations 
for each step that can be done in parallel.
'''

from __future__ import print_function
import numpy as np
from scipy import optimize
import argparse
import os
import sys
import argparse
import time
import findSim
from multiprocessing import Pool

scaleFactors = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0]

resultCount = 0
numIterations = 0
TOLERANCE = 0.001 # Don't want to go too tight on tolarance.

def reportReturn( result ):
    global resultCount
    print( ".", end = '' )
    sys.stdout.flush()
    resultCount += 1
    if resultCount % 50 == 0:
        print( " {}".format( resultCount ) )

def enumerateFindSimFiles( location ):
    if os.path.isdir( location ):
        if location[-1] != '/':
            location += '/'
        fnames = [ (location + i) for i in os.listdir( location ) if i.endswith( ".tsv" )]
        return fnames, [1.0] * len( fnames )
    elif os.path.isfile( location ):
        fnames = []
        weights = []
        with open( location, "r" ) as fp:
            for line in fp:
                if len( line ) <= 2:
                    continue
                if line[0] == '#':
                    continue
                f,w = line.split()
                fnames.append( f )
                weights.append( float( w ) )
        return fnames, weights
    else:
        print( "Error: Unable to find file or directory at " + location )
        quit()

class EvalFunc:
    def __init__( self, params, expts, weights, pool, modelFile ):
        self.params = params
        self.expts = expts
        self.weights = weights
        self.pool = pool # pool of available CPUs
        self.modelFile = modelFile

    def doEval( self, x ):
        ret = []
        assert( len(x) == len( self.params) )
        paramList = []
        for i, j in zip( self.params, x ):
            spl = i.split( '.' )
            assert( len(spl) == 2 )
            obj, field = spl
            paramList.append( obj )
            paramList.append( field )
            paramList.append( j )

        for k in self.expts:
            ret.append( self.pool.apply_async( findSim.innerMain, (k,), dict(modelFile = self.modelFile, hidePlot=True, silent=True, scaleParam=paramList), callback = reportReturn ) )
        score = [ i.get() for i in ret ]
        sumScore = sum([ s*w for s,w in zip(score, self.weights) if s>=0.0])
        sumWts = sum( [ w for s,w in zip(score, self.weights) if s>=0.0 ] )
        return sumScore/sumWts

def optCallback( x ):
    global numIterations
    numIterations += 1
    print ("\n***{} iterations: {}".format( numIterations, x ) )


def main():
    t0 = time.time()
    parser = argparse.ArgumentParser( description = 'Wrapper script to run a lot of FindSim evaluations in parallel.' )

    parser.add_argument( 'location', type = str, help='Required: Directory in which the scripts (in tsv format) are all located. OR: File in which each line is the filename of a scripts.tsv file, followed by weight to assign for that file.')
    parser.add_argument( '-n', '--numProcesses', type = int, help='Optional: Number of processes to spawn', default = 2 )
    parser.add_argument( '-m', '--model', type = str, help='Optional: Composite model definition file. First searched in directory "location", then in current directory.', default = "FindSim_compositeModel_1.g" )
    parser.add_argument( '-p', '--parameters', nargs='*', default=[],  help='Parameter to vary. Each is defined as an object.field pair. The object is defined as a unique MOOSE name, typically name or parent/name. The field is separated from the object by a period. The field may be concInit for molecules, Kf, Kb, Kd or tau for reactions, and Km or Kcat for enzymes. One can specify more than one parameter for a given reaction or enzyme. It is advisable to use Kd and tau for reactions unless you have a unidirectional reaction.' )
    parser.add_argument( '-f', '--file', type = str, help='Optional: File name for output of parameter minimization', default = "" )
    args = parser.parse_args()
    location = args.location
    if location[-1] != '/':
        location += '/'
    if os.path.isfile( location + args.model ):
        modelFile = location + args.model
    elif os.path.isfile( args.model ):
        modelFile = args.model
    else:
        print( "Error: Unable to find model file {}".format( args.model ) )
        quit()

    #fnames = [ (location + i) for i in os.listdir( args.location ) if i.endswith( ".tsv" )]
    fnames, weights = enumerateFindSimFiles( args.location )
    pool = Pool( processes = args.numProcesses )

    params = []
    for i in args.parameters:
        print( "{}".format( i ) )
        spl = i.split( '.' )
        assert( len(spl) == 2 )
        params.append( i )
    ev = EvalFunc( params, fnames, weights, pool, modelFile )
    results = optimize.minimize( ev.doEval, np.ones( len(params) ), tol = TOLERANCE, callback = optCallback )
    print( "\n----------- Completed in {:.3f} sec ---------- ".format(time.time() - t0 ) )
    print( "\n----- Score= {:.4f} ------ ".format(results.fun ) )
    dumpData = False
    fp = ""
    if len( args.file ) > 0:
        fp = open( args.file, "w" )
        dumpData = True
    analyzeResults( fp, dumpData, results, params )
    if dumpData:
        fp.close()

def analyzeResults( fp, dumpData, results, params ):
    #assert( len(results.x) == len( results.fun ) )
    assert( len(results.x) == len( params ) )
    for p,x, in zip(params, results.x):
        outputStr = "Parameter = {},\toptimized scale={:.3f}".format(p, x)
        print( outputStr )
        if dumpData:
            fp.write( outputStr + '\n' )
        
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
