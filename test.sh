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

$PYTHON findSim.py ./Curated/Jain2009_Fig3F.json --model models/synSynth7.g
$PYTHON findSim.py ./Curated/Bhalla1999_fig2B.json --model models/synSynth7.g
$PYTHON findSim.py ./Curated/Gu2004_fig3B.json --model models/synSynth7.g
$PYTHON findSim.py ./Curated/Bhalla1999_fig4C.json --model models/synSynth7.g
