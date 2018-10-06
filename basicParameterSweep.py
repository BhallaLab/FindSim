
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
 * File:            basicParameterSweep.py
 * Description:
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/

/**********************************************************************
** This program is part of 'FindSim', the
** Framework for Integrating Neuronal Data and SIgnaling Models
**           copyright (C) 2003-2018 Upinder S. Bhalla. and NCBS
**********************************************************************/

This script does a basic parameter sweep on the model. It runs the findSim 
program on all tsv files in the specified directory with modifications of
the selected parameters. It computes the mean score for each run and
presents the "best" (parameter, score) along with next-best flanking.
It can do this in parallel using Python's multiprocessing library.
'''

from __future__ import print_function
import numpy
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

def main():
    parser = argparse.ArgumentParser( description = 'Wrapper script to run a lot of FindSim evaluations in parallel.' )

    parser.add_argument( 'location', type = str, help='Required: Directory in which the scripts (in tsv format) are all located.')
    parser.add_argument( '-n', '--numProcesses', type = int, help='Optional: Number of processes to spawn', default = 2 )
    parser.add_argument( '-m', '--model', type = str, help='Optional: Composite model definition file. First searched in directory "location", then in current directory.', default = "FindSim_compositeModel_1.g" )
    parser.add_argument( '-p', '--parameter_sweep', nargs='*', default=[],  help='Does a parameter sweep in range 0.5-2x of each object.field pair.' )
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

    fnames = [ (location + i) for i in os.listdir( args.location ) if i.endswith( ".tsv" )]
    pool = Pool( processes = args.numProcesses )
    #ret = findSim.innerMain(fnames[0], hidePlot=True)

    argDict = {}
    for i in args.parameter_sweep:
        print( "{}".format( i ) )
        scaleDict = {}
        spl = i.split( '.' )
        assert( len(spl) == 2 )
        obj, field = spl
        for scale in scaleFactors:
            ret = []
            for k in fnames:
                ret.append( pool.apply_async( findSim.innerMain, (k,), dict(modelFile = modelFile, hidePlot=True, silent=True, scaleParam=[obj,field,str(scale)]), callback = reportReturn ) )
            scaleDict[scale] = ret
        argDict[i] = scaleDict
    
    results = {}
    for i in argDict:
        scaleDict = argDict[i]
        temp = {}
        for j in scaleDict:
            temp[j] = [ k.get() for k in scaleDict[j] ]
        results[i] = temp
    print( "\n---------------- Completed ----------------- " )
    for objfield in results:
        analyzeResults( objfield, results[objfield] )

def analyzeResults( name, results ):
    score = []
    scale = []
    for res in results:
        goodRes = [ x for x in results[res] if x >= 0.0 ]
        if len( goodRes ) > 0:
            score.append( sum(goodRes)/len(goodRes) )
            scale.append( res )

    if len(score) == 0:
        print( "-1 at {} with Q = 0".format(name) )
        return
    bestScore = min( score )
    bestScoreIndex = score.index( bestScore )
    # We want best, the scale of the best, if it is an extrema, and Q
    # Q = slope = (max - min)/abs(scaleMax - scaleMin)
    if len( score ) == 1:
        Q = 0
    else:
        worstScore = max(score)
        worstScoreIndex = score.index( worstScore )
        Q = (worstScore - bestScore)/abs(scale[bestScoreIndex] - scale[worstScoreIndex])
    print( "{}: {:3f} at {} with Q = {:3f}".format(name, bestScore, scale[bestScoreIndex],
        Q) )

        
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
