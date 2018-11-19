########################################################################
# This example demonstrates a multiscale model with synaptic input, Ca
# entry to the spine, receptor modulation following phosphorylation and 
# Ca diffusion from spine to the dendrite. Lots going on. 
# System switches to a potentiated state after a 1s strong synaptic input.
#
#   Ca+CaM <===> Ca_CaM;    Ca_CaM + CaMKII <===> Ca_CaM_CaMKII (all in 
#       spine head, except that the Ca_CaM_CaMKII translocates to the PSD)
#   chan ------Ca_CaM_CaMKII-----> chan_p; chan_p ------> chan  (all in PSD)
# 
# Copyright (C) Upinder S. Bhalla NCBS 2018
# Released under the terms of the GNU Public License V3.
########################################################################
import moose
import rdesigneur as rd
def load():
    rdes = rd.rdesigneur(
        elecDt = 50e-6,
        chemDt = 0.002,
        diffDt = 0.002,
        chemPlotDt = 0.02,
        turnOffElec = True, #FindSim needs to create Vclamp and then solver.
        useGssa = False,
        # cellProto syntax: ['ballAndStick', 'name', somaDia, somaLength, dendDia, dendLength, numDendSegments ]
        cellProto = [['ballAndStick', 'soma', 12e-6, 12e-6, 4e-6, 100e-6, 1 ]],
        chemProto = [['models/CaMKII_MAPK_7.g', 'chem']],
        spineProto = [['makeActiveSpine()', 'spine']],
        chanProto = [
            ['make_Na()', 'Na'], 
            ['make_K_DR()', 'K_DR'], 
            ['make_K_A()', 'K_A' ],
            ['make_glu()', 'glu' ],
            ['make_Ca()', 'Ca' ],
            ['make_Ca_conc()', 'Ca_conc' ]
        ],
        passiveDistrib = [['soma', 'CM', '0.01', 'Em', '-0.06']],
        spineDistrib = [['spine', '#dend#', '100e-6', '1e-6']],
        chemDistrib = [['chem', '#', 'install', '1' ]],
        chanDistrib = [
            ['Na', 'soma', 'Gbar', '300' ],
            ['K_DR', 'soma', 'Gbar', '250' ],
            ['K_A', 'soma', 'Gbar', '200' ],
            ['glu', 'dend#', 'Gbar', '20' ],
            ['Ca_conc', 'soma', 'tau', '0.0333' ],
            ['Ca', 'soma', 'Gbar', '40' ]
        ],
        adaptorList = [
            [ 'psd/tot_phospho_R', 'n', 'glu', 'modulation', 1.0, 0.3 ],
            [ 'Ca_conc', 'Ca', 'psd/Ca', 'conc', 0.00008, 3 ]
        ],
        # Syn wt is 0.2, specified in 2nd argument
        stimList = [['head#', '0.2','glu', 'periodicsyn', '0']],
    )
    moose.seed(1234567)
    rdes.buildModel()
    #moose.element( '/model/chem/dend/ksolve' ).numThreads = 4
    #moose.showfield( '/model/chem/dend/ksolve' )
    #moose.element( '/model/chem/dend/ksolve' ).method = "rk4"
    moose.delete( '/model/stims/stim0')
    inputElm = moose.element( '/model/elec/head0/glu/sh/synapse/synInput_rs' )
    inputElm.name = 'synInput'
    moose.connect( inputElm, 'spikeOut', '/model/elec/head0/glu/sh/synapse', 'addSpike' )
    #moose.showmsg( '/model/elec/head0/glu/sh/synapse/synInput_rs' )
    #import presettle_CaMKII_MAPK7_init
    moose.reinit()
    
    return rdes.model
