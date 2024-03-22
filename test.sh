#!/usr/bin/env bash

set -e 
set -x

# virtualenv does not require --user
PYTHON=$(which python)

$PYTHON findSim.py ./Curated/Jain2009_Fig3F.json --model models/synSynth7.g --map models/synSynth7_map.json --solver LSODA
$PYTHON findSim.py ./Curated/Bhalla1999_Fig2B.json --model models/synSynth7.g --map models/synSynth7_map.json --solver LSODA
$PYTHON findSim.py ./Curated/Gu2004_fig3B.json --model models/synSynth7.g --map models/synSynth7_map.json --solver LSODA
$PYTHON findSim.py ./Curated/Bhalla1999_Fig4C.json --model models/synSynth7.g --map models/synSynth7_map.json --solver LSODA
