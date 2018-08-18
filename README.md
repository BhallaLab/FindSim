# FindSim
Framework for Integration of Neuronal Data and SIgnaling Models.

The FindSim project maps models of neural and cellular signaling to 
experimental protocols and readouts. It runs the experiment on the model, and
provides a score that reports how closely the two match.

This file and the files in this repository are licensed under GPL v3 or later.

Quick start: 
A. Run one of the example experiments on the default model, generating a graph 
to compare model to experiment:

1. Install MOOSE (Instructions can be found here: http://moose.readthedocs.io/en/latest/install/install.html )
2. Install FindSim:
	git clone https://github.com/BhallaLab/FindSim
3. Navigate to release or to development branch, e.g.,
	cd ./FindSim/FindSim1.0.0
3. Run findSim on an example model:
	python findSim.py Curated/FindSim-Jain2009-Fig2B.tsv

B. Batch run of the entire set of curated experiments on 8 cores:
1. python runAllParallel.py Curated -n 8

C. Syntax help:
1. python findSim.py -h
2. python runAllParallel.py -h

=============================================================================
File organization:
FindSim: project directory
FindSim/FindSim1.x.x			: Tag Release directories
FindSim/FindSim1.x.x/Curated		: Curated experiment files
FindSim/FindSim1.x.x/models		: Model files
FindSim/FindSim1.x.x/findSim.py		: Main findSim script
FindSim/FindSim1.x.x/runAllParallel.py	: Batch/parallel wrapper script.
FindSim/FindSim1.x.x/runAllParallel.py	: Batch/parallel wrapper script.
FindSim/FindSim1.x.x/ExptSheet.xlsx	: Template worksheet with inline help
						and units, for Microsoft Excel.
FindSim/FindSim1.x.x/ExptSheet.ods	: Template worksheet with inline help
						and units, for Libre Office.
FindSim/FindSim1.x.x/ExptSchemaTimeSeries.xml	: Schema for tsv files 
						for time-series experiments.
FindSim/FindSim1.x.x/ExptSchemaDoseResp.xml	: Schema for tsv files 
						for Dose-response experiments.
FindSim/FindSim1.x.x/ExptSchemaMultiStim.xml	: Schema for tsv files 
						for multi-stimulus experiments.

FindSim/core				: Development branch. More features, 
						more models, more experiments,
						less stability.
FindSim/README.md			: This file

=============================================================================
Generating Figures for 
"FindSim: a Framework for Integrating Neuronal Data and Signaling Models."
by
Nisha A. Viswan, G.V. HarshaRani, Melanie I. Stefan, Upinder S. Bhalla
Currently in review.

All these are run using the tag branch FindSim1.0.0. Please cd into the
directory 
	FindSim/FindSim1.0.0
to run these.

Figure 6: bottom
python findSim.py Curated/FindSim-Jain2009-Fig????????????????????

Figure 7B:
python findSim.py Curated/X
python findSim.py Curated/Y

Figure 7C:
python findSim.py Curated/P

Figure 7D:
python findSim.py Curated/Q

=============================================================================
Other resources

The web template for experiment worksheet can be found here https://docs.google.com/spreadsheets/d/13J5jZD461OZjtJgsnXYnuXN7MRo9VQPE6JM3kbfrpIs/edit?usp=sharing

The MOOSE site:

MOOSE documentation:

Key papers used in the curated set of experiments:

DOQCS database, from which models were derived:

=============================================================================

To run FindSim script one needs to install moose which can be found here
https://moose.ncbs.res.in/readthedocs/install/install/install.html

To clone the FindSim repository use
  git clone https://github.com/BhallaLab/FindSim 
This will create folder called "FindSim" which contains
FindSim script, model files and Curated and NonCurated folder where experimental worksheets are stored.
`Curated` folder contains the FindSim worksheet which is tested again the model.
 `Non-Curated` worksheet which are yet to test.
 
 To run the script one need to run the command in python and synSynth7.g is the latest model that is tested out the worksheets.
 >python findSim.py Curated/worksheet.tsv --model (synSynth7.g) --hide_plot

runAllParallel.py script runs the findSim program on all tsv files in the specified directory, computes their scores, and prints out basic stats of the scores. It can do this in parallel using Python's multiprocessing library.

>python runAllParallel.py Directory (of tsv files) -n (Number of processes to spawn) --model (synSynth7.g)

