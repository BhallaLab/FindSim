import moose
import rdesigneur as rd
def load():
    rdes = rd.rdesigneur(
        turnOffElec = True,
        chanProto = [['make_HH_Na()', 'Na'], ['make_HH_K()', 'K']],
        chanDistrib = [
            ['Na', 'soma', 'Gbar', '1200' ],
            ['K', 'soma', 'Gbar', '360' ]],
    )
    rdes.buildModel()
    return rdes.model
