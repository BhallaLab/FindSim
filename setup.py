import os
import sys
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
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
    license='GPLv3'
)
