
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
 * File:            runAllParallel.py
 * Description:
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/

/**********************************************************************
** This program is part of 'MOOSE', the
** Messaging Object Oriented Simulation Environment,
**           copyright (C) 2003-2018 Upinder S. Bhalla. and NCBS
**********************************************************************/

This script runs the findSim program on all tsv files in the specified
directory, computes their scores, and prints out basic stats of the scores.
It can do this in parallel using Python's multiprocessing library.
'''

from __future__ import print_function
import numpy
import argparse
import os
import sys
import argparse
import time
import findSim
from multiprocessing import Pool

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

def main():
    t0 = time.time()
    parser = argparse.ArgumentParser( description = 'Wrapper script to run a lot of FindSim evaluations in parallel.' )

    parser.add_argument( 'location', type = str, help='Required: Directory in which the scripts (in tsv format) are all located.')
    parser.add_argument( '-n', '--numProcesses', type = int, help='Optional: Number of processes to spawn', default = 2 )
    parser.add_argument( '-m', '--model', type = str, help='Optional: Composite model definition file. First searched in directory "location", then in current directory.', default = "" )
    parser.add_argument( '-s', '--scale_param', nargs=3, default=[],  help='Scale specified object.field by ratio.' )
    args = parser.parse_args()
    location = args.location
    if location[-1] != '/':
        location += '/'
    if os.path.isfile( location + args.model ):
        modelFile = location + args.model
    elif args.model == "" or os.path.isfile( args.model ):
        modelFile = args.model
    else:
        print( "Error: runAllParallel: Unable to find model file '{}'".format( args.model ) )
        quit()

    fnames, weights = enumerateFindSimFiles( args.location )
    #fnames = [ (location + i) for i in os.listdir( args.location ) if i.endswith( ".tsv" )]
    pool = Pool( processes = args.numProcesses )
    #ret = findSim.innerMain(fnames[0], hidePlot=True)

    ret = [pool.apply_async( findSim.innerMain, (i,), dict(modelFile = modelFile, hidePlot=True, silent=True, scaleParam=args.scale_param, optimizeElec = False ), callback=reportReturn ) for i in fnames ]
    results = [ i.get() for i in ret ]
    numGood = 0
    sumScore = 0.0
    sumWts = 0.0
    print( "\n---------Completed---------\nScores = " )
    for i, j, w in zip( fnames, results, weights ):
        print( "{}  {:.3f}  {}".format( i, j, w ) )
        if j >= 0:
            numGood += 1
            sumScore += j * w
            sumWts += w
    print( "Weighted Score out of {:.0f} good runs = {:.3f}. Runtime = {:.3f} sec".format( numGood, sumScore / sumWts, time.time() - t0 ) )
        #print( "{0} : {1:.2f}".format( i, j ) )

        
# Run the 'main' if this script is executed standalone.
if __name__ == '__main__':
    main()
