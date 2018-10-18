
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
import numpy
from scipy import optimize
import argparse
import os
import sys
import argparse
import findSim
from multiprocessing import Pool

scaleFactors = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0]

resultCount = 0

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
    def __init__( self, objField, expts, weights, pool, modelFile, presettle = [] ):
        self.objField = objField
        self.expts = expts
        self.weights = weights
        self.pool = pool # pool of available CPUs
        self.modelFile = modelFile
        self.presettle = presettle

    def doEval( self, x ):
        ret = []
        spl = self.objField.split( '.' )
        assert( len(spl) == 2 )
        obj, field = spl

        settleDict = {}
        if len( self.presettle ) == 3:
            presettleTime = float( self.presettle[2] )
            if presettleTime > 0:
            #print("{}".format( self.presettle ) )
                settleDict = findSim.innerMain( self.presettle[0], modelFile = self.presettle[1], hidePlot=True, silent=True, scaleParam=[obj,field,str(x)], settleTime = presettleTime )
        #print( "Doing presettle, len = {}".format( len(settleDict) ) )

        for k in self.expts:
            ret.append( self.pool.apply_async( findSim.innerMain, (k,), dict(modelFile = self.modelFile, hidePlot=True, silent=True, scaleParam=[obj,field,str(x)], settleDict=settleDict ), callback = reportReturn ) )
        score = [ i.get() for i in ret ]
        sumScore = sum([ s*w for s,w in zip(score, self.weights) if s>=0.0])
        sumWts = sum( [ w for s,w in zip(score, self.weights) if s>=0.0 ] )
        return sumScore/sumWts


def main():
    parser = argparse.ArgumentParser( description = 'Wrapper script to run a lot of FindSim evaluations in parallel.' )

    parser.add_argument( 'location', type = str, help='Required: Directory in which the scripts (in tsv format) are all located. OR: File in which each line is the filename of a scripts.tsv file, followed by weight to assign for that file.')
    parser.add_argument( '-n', '--numProcesses', type = int, help='Optional: Number of processes to spawn', default = 2 )
    parser.add_argument( '-m', '--model', type = str, help='Optional: Composite model definition file. First searched in directory "location", then in current directory.', default = "FindSim_compositeModel_1.g" )
    parser.add_argument( '-p', '--parameter_optimize', nargs='*', default=[],  help='Does a parameter optimization for each specified object.field pair.' )
    parser.add_argument( '-ps', '--presettle', nargs=3, default=[],  help='Arguments: tsv_file, model_file, settle_time. Obtains values of all concentrations after a specified settle-time, so that all calculations for the optimization runs can be initialized to this presettled value. The tsv_file is to specify which subset of the model_file to use. This option is most useful in costly multiscale models.' )
    parser.add_argument( '-f', '--file', type = str, help='Optional: File name for output of parameter optimization', default = ""
    )
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

    results = {}
    for i in args.parameter_optimize:
        print( "{}".format( i ) )
        spl = i.split( '.' )
        assert( len(spl) == 2 )
        obj, field = spl
        ev = EvalFunc( i, fnames, weights, pool, modelFile, args.presettle )
        # Bounded method uses Bounded Brent method.
        results[i] = optimize.minimize_scalar( ev.doEval, method = 'bounded', bounds = (0.0, 100.0) )
        print( "\n Finished optimizing for " + i)
    print( "\n---------------- Completed ----------------- " )
    dumpData = False
    fp = ""
    if len( args.file ) > 0:
        fp = open( args.file, "w" )
        dumpData = True
    for objfield in results:
        analyzeResults( fp, dumpData, objfield, results[objfield] )
    if dumpData:
        fp.close()

def analyzeResults( fp, dumpData, name, result ):
    outputStr = "Parameter = {},    optimized scale={:.3f},     score = {:.3f}".format( name, result.x, result.fun )
    print( outputStr )
    if dumpData:
        fp.write( outputStr + '\n' )
        
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
