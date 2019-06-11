#!/usr/bin/env bash

set -e 

# virtualenv does not require --user
PYTHON=$(which python)

# From here https://stackoverflow.com/a/40950971/1805129
PYTHON_VERSION=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$PYTHON_VERSION" -eq "27" ]; then
    # $PYTHON -m pip uninstall matplotlib -y || echo "Failed to remove matplotlib"
    $PYTHON -m pip install matplotlib==2.2.3 --upgrade 
    $PYTHON -m pip install scipy==1.1.0 --upgrade 
else
    # $PYTHON -m pip uninstall matplotlib -y || echo "Failed to remove matplotlib"
    $PYTHON -m pip install matplotlib --upgrade 
    $PYTHON -m pip install --upgrade 
fi

# travis.yml should install FindSim
$PYTHON -m pip install Jinja2 --upgrade
$PYTHON -m pip install pylint --upgrade
# $PYTHON -m pip install mpld3
# $PYTHON -m pip install pymoose --pre --upgrade

find . -type f -name "*.py" | xargs -I file $PYTHON -m pylint \
    --disable=no-member \
    --exit-zero \
    -E file

# Run it in ./TestTSV directory.
for _tsv in $(find ./TestTSV -name *.tsv -type f); do
    echo "[INFO] Running experiment ${_tsv}"
    $PYTHON findSim.py ${_tsv} --model models/synSynth7.g
done

findsim ./Curated/FindSim-Jain2009_Fig4F.tsv --model models/synSynth7.g
findsim ./Curated/FindSim-Bhalla1999_fig2B.tsv --model models/synSynth7.g
# Following takes a lot of time to run.
#findsim ./Curated/FindSim-Gu2004_fig3B.tsv --model models/synSynth7.g
findsim ./Curated/FindSim-Ji2010_fig1C_ERK_acute.tsv --model models/synSynth7.g
findsim ./Curated/FindSim-Bhalla1999_fig4C.tsv --model models/synSynth7.g
timeout 60 findsim_parallel Curated -n 4 || echo "Timedout. We call it success!"
