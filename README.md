
[![Build Status](https://travis-ci.org/BhallaLab/FindSim.svg?branch=stable)](https://travis-ci.org/BhallaLab/FindSim)

# FindSim

Framework for Integration of Neuronal Data and SIgnaling Models. The associated paper is available 
at [https://doi.org/10.3389/fninf.2018.00038](https://doi.org/10.3389/fninf.2018.00038)

# About

The FindSim project maps models of neural and cellular signaling to 
experimental protocols and readouts. It runs the experiment on the model, and
provides a score that reports how closely the two match.
FindSim Experiments is moved from TSV file format to Json format
# LICENSE
This file and the files in this repository are licensed under GPL v3 or later.

# Version
Latest release is 

- **LegacyVersion1.2.0**

	We have moved our Experiment datasheet from TSV file format to Json file format and moose-core which is our primary backend simulation tool will be compiled using Python3, as Python 2 is no longer supported by the Python Software Foundation,
    This version of the FindSim code is tested against python2 and python3 with moose-core,
    *	<a href="https://github.com/BhallaLab/moose-core/commit/0ee20b3cd9ff9">BhallaLab/moose-core @ 0ee20b3cd9ff9</a> compiled with python3 and FindSim scripts run using python3.
    *	<a href="https://github.com/BhallaLab/moose-core/commit/2062ab231ff8fcc0644db4b5e054a3c571312bc2">BhallaLab/moose-core @ 2062ab2</a> version (tag Version <a href="https://github.com/BhallaLab/moose-core/releases/tag/FindSim-1.0-beta">FindSim-1.0-beta</a>) compiled with python2 and FindSim scripts run using python2.
    One can download FindSim scripts 
		*    https://github.com/BhallaLab/FindSim/archive/LegacyVersion1.2.0.zip
		*    https://github.com/BhallaLab/FindSim/archive/LegacyVersion1.2.0.tar.zip
- **1.1.0**

    FindSim Version v1.10 scripts for the paper was run with <a href="https://github.com/BhallaLab/moose-core/commit/12cf83e17ae8ca3111441ff1899c3cd67cbc30dd">moose-core</a> version or tag <a href=https://github.com/BhallaLab/moose-core/releases/tag/FindSim_1.0-alpha>FindSim-1.0-alpha</a> with python2, libsbml L3V.
    Later the same scripts were run with latest code of <a href="https://github.com/BhallaLab/moose-core/commit/2062ab231ff8fcc0644db4b5e054a3c571312bc2">moose-core</a> version or tag version <a href=https://github.com/BhallaLab/moose-core/releases/tag/FindSim-1.0-beta> FindSim-1.0-beta</a> with python2 and found the result matched as documented in the paper. 
    FindSim version v1.1.0 can be downloadable at 
	- https://github.com/BhallaLab/FindSim/archive/v1.1.0.zip <br> 
	- https://github.com/BhallaLab/FindSim/archive/v1.1.0.tar.gz


# Install 
	To run FindSim script one needs to  
		- Install MOOSE which can be found here  
			https://moose.ncbs.res.in/readthedocs/install/install.html  
		- Install FindSim:  
			Clone the entire repository using  
  				>git clone https://github.com/BhallaLab/FindSim 
			or, clone specific branch such as "stable" or "develop" using:
				>git clone -b <branch-name> https://github.com/BhallaLab/FindSim

=============================================================================
# File organization:
	After successful cloning, the directory structure goes as follows,
	FindSim/             			: project directory  
	FindSim/stable				: Stable branch. Stable version of `develop` branch  
	FindSim/Curated				: Folder contains FindSim worksheets to which the model is well fit.
	FindSim/Non-Curated			: Folder contains FindSim worksheets which is yet to curate.
	FindSim/TestJson			: Folder contains examples of FindSim worksheets to which the model is well fit.
	FindSim/models				: Model files and mapping file
	FindSim/findSim.py			: Main findSim script to read Json format  
	FindSim/findSimSchema.json		: FindSim Schema definition
	FindSim/runAllParallel.py		: Batch/parallel wrapper script.  
	FindSim/FindSim-Schema.json		: Schema for Json files for worksheet.  
	FindSim/README.md			: This file  
						
=============================================================================
# Quick start: 
FindSim comes in two versions. One (findSim.py) runs single experiment and one (runAllParallel.py) for batch processing of experiments.
A. findSim.py script run one of the example experiments on the default model, generating a graph to compare model to experiment:  
To run the script, run the command in python and `synSynth7.g` is the latest model that is tested out the worksheets.  One can also pass the model explicitly

>python findSim.py Curated/Jain2009-Fig2B.json <br> 
					or <br>
>python findSim.py Curated/Jain2009-Fig2B.json --model models/synSynth7.g --map models/synSynth7_map.json <br>
	  				or  <br>
>python findSim2.py Curated/Jain2009-Fig2B.json --map models/synSynth7_map.json

B. Batch run:  
	runAllParallel.py script runs the findSim program on all experiment files in the specified directory, computes their scores, and prints out basic stats of the scores. It can do this in parallel using Python's multiprocessing library.  
	
	>python runAllParallel.py Curated -n 8  (run of the entire set of `Curated` experiments on 8 cores)
It will run the entire set of `Curated` experiments in parallel using 8 independant processes (it will be effectively if your computer has at least 8 cores). The value of `-n` should not be more than `N+1` where `N` is the number of processors on your system (use system utility `nproc` to see this number).
								 
	>python runAllParallel.py Directory (of json files) -n (Number of processes to spawn) --model (synSynth7.g)  

C. To see the help message, pass '-h' option to either of these commands.  
>python findSim.py -h  
>python runAllParallel.py -h  

	`findsim -h` will show you following message.
	usage: findsim [-h] [-m MODEL] [-d DUMP_SUBSET] [-p PARAM_FILE] [-t] [-hp]
               [-hs] [-o] [-s SCALE_PARAM SCALE_PARAM SCALE_PARAM]
               [-settle_time SETTLE_TIME]
               script
    FindSim argument parser This program loads a kinetic model, and runs it with 
    the specified stimuli. The output is then compared with expected output 
    specified in the same file, to generate a model score.
    positional arguments:
    script                	Required: filename of experiment spec, in tsv format.
    optional arguments:
    -h, --help            	show this help message and exit
    -map MAP, --map MAP   	Optional: mapping file from tsv names to sim-specific strings. JSON format
    -m MODEL, --model MODEL 	[Optional: model filename, .g or .xml]
    -d DUMP_SUBSET, --dump_subset DUMP_SUBSET
	                        Optional: dump selected subset of model into named file
    -p PARAM_FILE, --param_file PARAM_FILE
	                        Optional: Generate file of tweakable params belonging to selected subset of model
    -t, --tabulate_output
	                        Flag: Print table of plot values. Default is NOT to print table
    -hp, --hide_plot      	Hide plot output of simulation along with expected values. Default is to show plot.
    -hs, --hide_subplots  	Hide subplot output of simulation. By default the graphs include dotted lines to indicate individual quantities (e.g., states of a molecule) that are being summed to give a total response. This flag turns off just those dotted lines, while leaving the main plot intact.
    -o, --optimize_elec   	Optimize electrical computation. By default the electrical computation runs for the entire duration of the simulation. With this flag the system turns off the electrical engine except during the times when electrical stimuli are being given. This can be *much* faster.
    -s SCALE_PARAM SCALE_PARAM SCALE_PARAM, --scale_param SCALE_PARAM SCALE_PARAM SCALE_PARAM
	                        Scale specified object.field by ratio.
    -settle_time SETTLE_TIME, --settle_time SETTLE_TIME
	                        Run model for specified settle time and return dict of {path,conc}.
=============================================================================

Generating Figures for   
"FindSim: a Framework for Integrating Neuronal Data and Signaling Models."  
by Nisha A. Viswan, G.V. HarshaRani, Melanie I. Stefan, Upinder S. Bhalla
Front Neuroinform. 2018 Jun 26;12:38. doi: 10.3389/fninf.2018.00038. eCollection 2018.

All these are run using the <a href="https://github.com/BhallaLab/FindSim/releases/tag/v1.1.0">`release.1.1.0`</a>  
Please change into the branch to run these.  

Figure 6: bottom  
python findSim.py Curated/FindSim-Jain2009_Fig4F.tsv --model models/synSynth7.g  

Figure 7B:  
python findSim.py Curated/FindSim-Bhalla1999_fig2B.tsv --model models/synSynth7.g  
python findSim.py Curated/FindSim-Gu2004_Fig3.tsv --model models/synSynth7.g  

Figure 7C:  
python findSim.py Curated/FindSim-Ji2010_fig1C_ERK_acute.tsv --model models/synSynth7.g  

Figure 7D:  
python findSim.py Curated/FindSim-Bhalla1999_fig4C.tsv --model models/synSynth7.g  

=============================================================================
# Other resources
Project is hosted at https://github.com/BhallaLab/FindSim

The web template for experiment worksheet can be found here https://www.ncbs.res.in/faculty/bhalla-findsim/worksheet  

The MOOSE site: http://moose.ncbs.res.in  

MOOSE documentation: http://moose.ncbs.res.in/readthedocs/install/index_install.html  

Two papers were used as the initial basis for the models, and which in turn
refer to a large number of experimental studies for their data:  
	- Bhalla US., Iyengar R. Emergent properties of networks of biological signaling pathways. Science. 1999 Jan 15;283(5400):381-7.  
	- Jain P, and Bhalla, U.S. Signaling logic of activity-triggered dendritic protein synthesis: an mTOR gate but not a feedback switch. PLoS Comput Biol. 2009 Feb;5(2):e1000287. Epub 2009 Feb 13  

Two further papers were used for some of the experiments:  
	- Gu J, et al. Beta1,4-N-Acetylglucosaminyltransferase III down-regulates neurite outgrowth induced by costimulation of epidermal growth factor and integrins through the Ras/ERK signaling pathway in PC12 cells. Glycobiology. 2004 Feb;14(2):177-86. Epub 2003 Oct 23  
	- Ji Y, et al. Acute and gradual increases in BDNF concentration elicit distinct signaling and functions in neurons. Nat Neurosci. 2010 Mar;13(3):302-9. doi: 10.1038/nn.2505. Epub 2010 Feb 21.  

DOQCS database, from which models were derived: http://doqcs.ncbs.res.in  
	Sivakumaran S. et al. The Database of Quantitative Cellular Signaling: management and analysis of chemical kinetic models of signaling networks.
Bioinformatics. 2003. 19(3):408–415

