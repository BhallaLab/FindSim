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
 * File:            hillTau.py
 * Description:
 * Author:          Upinder S. Bhalla
 * E-mail:          bhalla@ncbs.res.in
 ********************************************************************/
 '''
from __future__ import print_function
import sys
import json
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt

lookupQuantityScale = { "M": 1000.0, "mM": 1.0, "uM": 1e-3, "nM": 1e-6, "pM": 1e-9 }

SIGSTR = "{:.4g}" # Used to format floats to keep to 4 sig fig. Helps when dumping JSON files.

def loadHillTau( fname ):
    with open( fname ) as json_file:
        model = json.load( json_file )
    return model

def subsetModel( model, subsetInfo ):
    return

class Stim():
    def __init__( self, stim, model, off = False ):
        self.objname = stim[0]
        self.mol = model.molInfo.get( stim[0] )
        if not self.mol:
            print( "Stimulus Molecule '{}' not found".format( stim[0] ) )
            quit()
        self.value = stim[1]
        self.isOff = off
        if off:
            self.time = stim[3]
            self.value = self.mol.concInit
        else:
            self.time = stim[2]

    @staticmethod
    def stimOrder( stim ):
        return stim.time


class MolInfo():
    def __init__( self, name, grp, order = 0, concInit = 0.0 ) :
        self.name = name
        self.grp = grp
        self.concInit = concInit
        self.order = order  # First pass: species, subs:0 Reac or Eqn -1
                        # Second pass: cumulative order depending on subs
        self.index = 0  # Points to the conc and concInit vectors
        #print( "MolInfo {}: concInit = {}".format( name, concInit ) )

class ReacInfo():
    def __init__( self, name, grp, reacObj, molInfo ):
        self.name = name
        self.grp = grp
        self.KA = reacObj["KA"]
        self.tau = reacObj["tau"]
        self.tau2 = self.tau
        self.prdIndex = molInfo[ name ].index
        self.subs = reacObj["subs"]
        assert( len( self.subs ) > 0 )
        if len( self.subs ) == 0:
            raise( ValueError( "Error: Reaction {} has zero reagents.".format( name ) ) )
        self.hillIndex = molInfo[ self.subs[-1] ].index
        self.reagIndex = molInfo[ self.subs[0] ].index
        # subIndices are all but the hillIndex.
        subIndices = [ molInfo[s].index for s in self.subs if s != self.subs[-1] ]
        if len( subIndices ) > 1:
            raise( ValueError( "Error: Reaction {} has {} reagents. Only single reagent R allowed.\nMust be of form R + nL <==> P or nL <==> P.".format( name, len( subIndices ) ) ) )

        # Hill Coeff applies only to the last mol in the list.
        self.oneSub = ( self.subs[0] == self.subs[-1] )
        self.HillCoeff = len( self.subs ) + self.oneSub - 1
        self.kh = self.KA ** self.HillCoeff # Precompute it.
        self.inhibit = 0
        inh = reacObj.get( "inhibit" )
        if inh and inh != 0:
            self.inhibit = 1
        self.baseline = 0.0
        b = reacObj.get( "baseline" )
        if b:
            self.baseline = b
        tau2 = reacObj.get( "tau2" )
        if tau2:
            self.tau2 = tau2

        #print( "Reac {}: hillIndex={}, hillCoeff = {}, kh = {}, reagIndex  {}".format( self.name, self.hillIndex, self.HillCoeff, self.kh, self.reagIndex ) )

    def concInf( self, conc ):
        h = conc[self.hillIndex] ** self.HillCoeff
        if self.oneSub: # this really only works for A<=>B and 2A<=>B
            return h / ( (h+self.kh) * self.HillCoeff )
        s = conc[ self.reagIndex ]
        if self.inhibit:
            #print( self.name, s, h, self.kh )
            return s * (1.0 - h / ( h + self.kh ) )
        else:
            return s * h / ( h + self.kh )

    def concFracUp( self, t ):
        return 1.0 - np.exp( -t/self.tau )

    def concFracDown( self, t ):
        return 1.0 - np.exp( -t/self.tau2 )

    def eval( self, model, dt ):
        orig = model.conc[self.prdIndex] - self.baseline
        delta = self.concInf( model.conc ) - orig
        if delta >= 0:
            delta *= self.concFracUp( dt )
        else:
            delta *= self.concFracDown( dt )
        ret = self.baseline + orig + delta
        if ret < 0.0:
            print( "Error: negative value on: ", self.name, ret, model.conc[self.prdIndex], self.baseline, delta )
            quit()
        model.conc[self.prdIndex] = ret
        return ret
    
    def getReacField( self, field ):
        return 0.0

class EqnInfo():
    def __init__( self, name, grp, eqnStr ):
        self.name = name
        self.grp = grp
        self.eqnStr = eqnStr
        self.subs = []

    @staticmethod
    def findMolToken( eqn ):
        ''' Finds the first molecule name in the given equation string.
        The first char must be an alphabetic one. 
        The subsequent chars must be alphabetic or _ (underscore).
        Returns the molecule name and the remainder of the string.
        '''
        isInMol = False
        start = 0
        for i, char in enumerate( eqn ):
            if not isInMol:
                if char.isalpha():
                    isInMol = True
                    start = i
                else:
                    continue
            else:
                if char.isalnum() or char == "_":
                    continue
                else:
                    return( eqn[start:i], eqn[i:] )
        if isInMol:
            return( eqn[start:], "" )
        else:
            return( "", eqn )
            
    def parseEqn( self, molInfo ):
        self.index = molInfo[self.name].index
        mol, eqn = EqnInfo.findMolToken( self.eqnStr )
        #print( "findMolToken in {} = '{}'  '{}'".format( self.eqnStr, mol, eqn))
        self.newEq = self.eqnStr
        while len( mol ) > 0:
            if mol in ["exp", "log", "tanh", "sqrt", "pow"]:
                self.newEq = self.newEq.replace( mol, "np.{}".format( mol ), 1 )
                mol, eqn = EqnInfo.findMolToken( eqn )
                continue
            mi = molInfo.get( mol )
            if not mi:
                print( "Error: unknown molecule '{}' in equation '{}'".format( mol, self.eqnStr ) )
                quit()
            self.newEq = self.newEq.replace( mol, "m[{}]".format( mi.index ), 1 )
            self.subs.append( mol )
            mol, eqn = EqnInfo.findMolToken( eqn )

    def eval( self, m ):
        m[self.index] = ret = eval( self.newEq )
        return ret

class Model():
    def __init__( self, jsonDict ):
        self.jsonDict = jsonDict
        self.molInfo = {}
        self.reacInfo = {}
        self.eqnInfo = {}
        self.sortedReacInfo = []
        self.currentTime = 0.0
        self.conc = np.zeros(1)
        self.concInit = np.zeros(1)
        self.plotvec = []
        self.runtime = 0.0
        self.dt = 1.0

    '''
    def setConc( self, molName, val ):
        assert( molName in self.molInfo )
        idx = self.molInfo[ molName ].index
        self.conc[idx] = val
    '''
    def advance( self, runtime, settle = False ):
        if runtime < 10e-6:
            return
        if settle: 
            # This is used when we are doing a steady-state calc. Since
            # HillTau does this anyway, we jump fast. Only issue arises
            # if there are feedback processes. So to be conservative, 
            # do 10 steps. 
            dt = runtime / 10.0
            ratio = 10 
        else:
            dt = self.dt
            if dt >= runtime / 2.0:
                dt = 10 ** ( np.floor( np.log10( runtime / 2.0 ) ) )
                #print( "adjusting local dt to ", dt, " from ", runtime )
            ratio = int( np.round( self.dt / dt ) )
        i = 0
        for t in np.arange( 0.0, runtime, dt ):
            for name, val in self.reacInfo.items():
                val.eval( self, dt )
            for name, val in self.eqnInfo.items():
                val.eval( self.conc )
            # This is a tricky aspect of Python: unless you force a copy of
            # the self.conc array, it just appends a pointer to it.
            if i % ratio == 0:
                self.plotvec.append( np.array( self.conc ) )
            i += 1
        self.currentTime += runtime

    def reinit( self ):
        # ConcInit is evaluated only for reactions not explicitly defined.
        self.currentTime = 0
        for ar in self.sortedReacInfo:
            for r in ar:
                if self.molInfo[ r.name ].order < 0:
                    if r.inhibit:
                        self.concInit[ r.prdIndex ] = r.concInf( self.concInit ) + r.baseline
                        if self.concInit[r.prdIndex] < 0.0:
                            #print( "oops, starting -ve:", r.name, self.concInit[r.prdIndex] )
                            self.concInit[r.prdIndex] = 0.0

                    else:
                        self.concInit[ r.prdIndex ] = r.baseline
        # need to do this because Python defaults to shallow copy.
        # So if you change values in conc, they will change in concInit
        self.conc = np.array( self.concInit )
        del self.plotvec[:]
        self.plotvec.append( np.array( self.conc ) )

def getQuantityScale( jsonDict ): 
    qu = jsonDict.get( "quantityUnits" )
    qs = 1.0
    if qu:
        qs = lookupQuantityScale[qu]
    return qs

def scaleDict( jsonDict, qs ):
    for grpname, grp in jsonDict["Groups"].items():
        sp = grp.get( "Species" )
        if sp:
            for m in sp:
                sp[m] = float( SIGSTR.format( sp[m] * qs ) )
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                reac["KA"] = float( SIGSTR.format( reac["KA"] * qs ) )
                reac["tau"] = float( SIGSTR.format( reac["tau"] ) )
                tau2 = reac.get( "tau2" )
                if tau2:
                    reac["tau2"] = float( SIGSTR.format( tau2 ) )
                bl = reac.get( "baseline" )
                if bl:
                    reac["baseline"] = float( SIGSTR.format( bl * qs ) )

def parseModel( jsonDict ):
    model = Model( jsonDict )

    # First, pull together all the species names. They crop up in
    # the Species, the Reacs, and the Eqns. They should be used as
    # an index to the conc and concInit vector.
    # Note that we have an ordering to decide which mol goes in which group:
    # Species; names of reacs, First term of Eqns, substrates.
    # This assumes that every quantity term has already been scaled to mM.
    for grpname, grp in model.jsonDict['Groups'].items():
        # We may have repeats in the species names as they are used 
        # in multiple places.
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                for subname in reac["subs"]:
                    model.molInfo[subname] = MolInfo( subname, grpname, order=0)

    for grpname, grp in model.jsonDict['Groups'].items():
        if "Eqns" in grp:
            for lhs, expr in grp["Eqns"].items():
                model.eqnInfo[lhs] = EqnInfo( lhs, grpname, expr )
                model.molInfo[lhs] = MolInfo( lhs, grpname, order=-1)
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                model.molInfo[reacname] = MolInfo( reacname, grpname, order=-1 )

    for grpname, grp in model.jsonDict['Groups'].items():
        if "Species" in grp:
            for molname, conc in grp['Species'].items():
                model.molInfo[molname] = MolInfo( molname, grpname, order=0, concInit = conc )
                grp['Species'][molname] = conc

    # Then assign indices to these unique molnames, and build up the
    # numpy arrays for concInit and conc.
    numMols = len( model.molInfo )
    model.conc = np.zeros( numMols )
    model.concInit = np.zeros( numMols )
    i = 0
    for molname, info in model.molInfo.items():
        info.index = i
        model.conc[i] = model.concInit[i] = info.concInit
        i += 1

    # Now set up the reactions. we need the mols all defined first.
    for grpname, grp in model.jsonDict['Groups'].items():
        if "Reacs" in grp:
            for reacname, reac in grp['Reacs'].items():
                r = ReacInfo( reacname, grpname, reac, model.molInfo )
                model.reacInfo[reacname] = r
                # Eval concInit ONLY if it is not explicitly defined.
                if model.molInfo[ reacname ].order == -1:
                    if r.inhibit:
                        model.concInit[ r.prdIndex ] = r.concInf( model.concInit ) + r.baseline
                        if model.concInit[r.prdIndex] < 0.0:
                            #print( "oops, starting -ve:", r.name, self.concInit[r.prdIndex] )
                            model.concInit[r.prdIndex] = 0.0
                    else:
                        model.concInit[ r.prdIndex ] = r.baseline

    # Now set up the equation, again, we need the mols defined.
    for eqname, eqn in model.eqnInfo.items():
        eqn.parseEqn( model.molInfo )

    model.reinit()
    sortReacs( model )
    return model

def breakloop( model, maxOrder, numLoopsBroken  ):
    for reacname, reac in model.reacInfo.items():
        if model.molInfo[reacname].order < 0:
            model.molInfo[reacname].order = maxOrder
            #print("Warning; Reaction order loop. Breaking {} loop for {}, assigning order: {}".format( numLoopsBroken, reacname, maxOrder ) )
            break

def sortReacs( model ):
    # Go through and assign levels to the mols and reacs within a group.
    # This will be used later for deciding evaluation order.
    numOrdered = sum( [ ( m.order >= 0 ) for m in model.molInfo.values() ] )
    maxOrder = 0
    numLoopsBroken = 0
    while numOrdered < len( model.molInfo ): 
        stuck = True
        for reacname, reac in sorted( model.reacInfo.items() ):
            order = [ model.molInfo[i].order for i in reac.subs ]
            #print( "{}@{}: {}".format( reacname, model.molInfo[reacname].order, order ) )
            if min( order ) >= 0:
                mo = max( order ) + 1
                model.molInfo[reacname].order = mo
                maxOrder = max( maxOrder, mo )
                numOrdered += 1
                stuck = False
        if stuck:
            breakloop( model, maxOrder, numLoopsBroken )
            numLoopsBroken += 1
            #quit()

        for eqname, eqn in sorted( model.eqnInfo.items() ):
            order = [ model.molInfo[i].order for i in eqn.subs ]
            model.molInfo[eqname].order = max(order)

    maxOrder += 1
    model.sortedReacInfo = [[]] * maxOrder    
    for name, reac in model.reacInfo.items():
        order = model.molInfo[name].order
        model.sortedReacInfo[order].append( reac )

def main():
    parser = argparse.ArgumentParser( description = 'hillTau simulator\n'
    'This program simulates abstract kinetic/neural models defined in the\n'
    'HillTau formalism. HillTau is an event-driven JSON form to represent\n'
    'dynamics of mass-action chemistry and neuronal activity in a fast, \n'
    'reduced form. The hillTau program loads and checks HillTau models,\n'
    'and optionally does rudimentary stimulus specification and plotting\n')
    parser.add_argument( 'model', type = str, help='Required: filename of model, in JSON format.')
    parser.add_argument( '-r', '--runtime', type = float, help='Optional: Run time for model, in seconds. If flag is not set the model is not run and there is no display', default = 0.0 )
    parser.add_argument( '-s', '--stimulus', type = str, nargs = '+', action='append', help='Optional: Deliver stimulus as follows: --stimulus molecule conc [start [stop]]. Any number of stimuli may be given, each indicated by --stimulus. By default: start = 0, stop = runtime', default = [] )
    parser.add_argument( '-p', '--plots', type = str, help='Optional: plot just the specified molecule(s). The names are specified by a comma-separated list.', default = "" )
    args = parser.parse_args()
    jsonDict = loadHillTau( args.model )
    scaleDict( jsonDict, getQuantityScale( jsonDict ) )
    model = parseModel( jsonDict )

    runtime = args.runtime
    if runtime <= 0.0:
        return

    model.dt = 10 ** (np.floor( np.log10( runtime )) - 2.0)
    if runtime / model.dt > 500:
        model.dt *= 2

    stimvec = []
    
    for i in args.stimulus:
        if len( i ) < 2:
            print( "Warning: need at least 2 args for stimulus, got {i}".format( i ) )
            continue
        i[1] = float( i[1] )
        if len(i) == 2:
            i.extend( [0.0, runtime] )
        if len(i) == 3:
            i.extend( [runtime] )
        i[2] = float( i[2] )
        i[3] = float( i[3] )
        runtime = max( runtime, i[3] )
        stimvec.append( Stim( i, model ) )
        stimvec.append( Stim( i, model, off = True ) )

    stimvec.sort( key = Stim.stimOrder )

    model.reinit()
    currTime = 0.0
    for s in stimvec:
        model.advance( s.time - currTime )
        model.conc[s.mol.index] = s.value
        #print( "STIM: ", s.name, s.value )
        currTime = s.time
    if runtime > currTime:
        model.advance( runtime - currTime )

    plotvec = np.transpose( np.array( model.plotvec ) )
    x = np.array( range( plotvec.shape[1] ) ) * model.dt
    clPlots = args.plots.split(',')
    if len( args.plots ) > 0 :
        clPlots = [ i.strip() for i in clPlots if i in model.molInfo]
    else: 
        clPlots = [ i for i in model.molInfo ]

    for name in clPlots:
        mi = model.molInfo[name]
        i = mi.index
        plt.plot( x, plotvec[i], label = name )

    '''
    for name, mi in model.molInfo.items():
        i = mi.index
        plt.plot( x, plotvec[i], label = mi.name )
    '''

    plt.xlabel('Time (s)')
    plt.ylabel('Conc (uM)')
    plt.title( args.model )
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
