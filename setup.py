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
        name = "findsim",
        version = "1.0.0",
        description = "A Framework for Integrating Neuronal Data and Singalling Model",
        long_description = readme,
        long_description_content_type = "text/markdown",
        packages = [ "findsim" ],
        package_dir = { "findsim" : "."},
        install_requires = [ 'pymoose', 'scipy' ],
        author = "Dilawar Singh",   # author of packaging. See contributors for
        # autor of findsime
        author_email = "dilawar@ncbs.res.in",
        url = "http://github.com/BhallaLab/FindSime",
        package_data = { "findsim" : [ '*.csv' ] },
        license='GPLv3',
        entry_points = {
            'console_scripts' : [
                'findsim = findsim.__main__:run',
                'findsim_parallel = findsim.__main__:run_parallel'
                ]
            },
        )
