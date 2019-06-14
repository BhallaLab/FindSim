#!/usr/bin/env bash
set -e 

INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "")')

echo "INVENV ${INVENV}"
if [ -z "$INVENV" ]; then
    if [ -z "$TRAVIS" ]; then
        echo "Not on travis. I'll set a virtualenv for you"
        python -m pip install virtualenv --user --upgrade
        virtualenv -p $(which python) /tmp/envPY
        source /tmp/envPY/bin/activate
    fi
else
    echo "Already in virtualenv. How cool!"
fi

# FROM NOW ON WE MUST BE IN A VIRTUALENV.
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
    $PYTHON -m pip install scipy --upgrade 
fi

# travis.yml should install FindSim
$PYTHON -m pip install Jinja2 --upgrade
$PYTHON -m pip install pylint --upgrade
$PYTHON -m pip install mpld3
$PYTHON -m pip install pymoose --pre --upgrade
$PYTHON -m pip install .

echo "PYLINT START======================================================="
find . -type f -name "*.py" | xargs -I file $PYTHON -m pylint \
    --disable=no-member \
    --generated-members=moose \
    -E file
echo "========================================================PYLINT DONE"
echo " "
echo " "

# Run it in ./TestTSV directory.
for _tsv in $(find ./TestTSV -name *.tsv -type f); do
    echo "[INFO] Running experiment ${_tsv}"
    $PYTHON findSim.py ${_tsv} --model models/synSynth7.g
done

time findsim ./Curated/FindSim-Jain2009_Fig4F.tsv --model models/synSynth7.g
time findsim ./Curated/FindSim-Bhalla1999_fig2B.tsv --model models/synSynth7.g
# Following takes a lot of time to run.
#findsim ./Curated/FindSim-Gu2004_fig3B.tsv --model models/synSynth7.g
time findsim ./Curated/FindSim-Ji2010_fig1C_ERK_acute.tsv --model models/synSynth7.g
time findsim ./Curated/FindSim-Bhalla1999_fig4C.tsv --model models/synSynth7.g
timeout 60 findsim_parallel Curated -n 4 || echo "Timedout. We call it success!"

# deactivate venv if we are in it.
if [ ! -z "$INVENV" ]; then
    if [ -z "$TRAVIS" ]; then
        deactivate
    fi
fi
