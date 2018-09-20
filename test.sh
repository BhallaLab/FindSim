#!/usr/bin/env bash

set -e 
set -x

# virtualenv does not require --user
PYTHON=$(which python)

$PYTHON -m pip install pymoose --pre --upgrade
$PYTHON -m pip install pylint numpy --upgrade 

find . -type f -name "*.py" | xargs -I file $PYTHON -m pylint \
    --disable=no-member \
    --exit-zero \
    -E file

$PYTHON findSim.py ./Curated/FindSim-Jain2009_Fig4F.tsv --model models/synSynth7.g
$PYTHON findSim.py ./Curated/FindSim-Bhalla1999_fig2B.tsv --model models/synSynth7.g
$PYTHON findSim.py ./Curated/FindSim-Gu2004_fig3B.tsv --model models/synSynth7.g
$PYTHON findSim.py ./Curated/FindSim-Ji2010_fig1C_ERK_acute.tsv --model models/synSynth7.g
$PYTHON findSim.py ./Curated/FindSim-Bhalla1999_fig4C.tsv --model models/synSynth7.g
