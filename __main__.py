"""__main__.py: 

Entry point for this package.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"


def run():
    from FindSim import findSim
    findSim.main()

def run_parallel():
    from FindSim import runAllParallel
    runAllParallel.main()

if __name__ == '__main__':
    run()
