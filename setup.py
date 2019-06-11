"""setup.py: 
    Packaging script for FindSim.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import os
import sys
import setuptools

with open("README.md") as f:
    readme = f.read()

setuptools.setup(
        name = "FindSim",
        version = "1.0.0",
        description = "A Framework for Integrating Neuronal Data and Singalling Model",
        long_description = readme,
        long_description_content_type = "text/markdown",
        packages = [ "FindSim" ],
        package_dir = { "FindSim" : "."},
        install_requires = [ 'pymoose', 'scipy' ],
        author = "Dilawar Singh",   # author of packaging. See contributors for
                                    # the list of authors 
        author_email = "dilawar@ncbs.res.in",
        url = "http://github.com/BhallaLab/FindSime",
        package_data = { "FindSim" : [ '*.csv', '*.xml' ] },
        include_pacakge_data  = True,
        license='GPLv3',
        entry_points = {
            'console_scripts' : [
                'findsim = FindSim.__main__:run',
                'findsim_parallel = FindSim.__main__:run_parallel'
                ]
            },
        )
