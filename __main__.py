"""__main__.py: 

Entry point for this package.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import findSim
import runAllParallel

def run():
    findSim.main()

def run_parallel():
    runAllParallel.main()

if __name__ == '__main__':
    run()
