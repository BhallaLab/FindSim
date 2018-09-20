[![Build Status](https://travis-ci.org/BhallaLab/FindSim.svg?branch=stable)](https://travis-ci.org/BhallaLab/FindSim)

# FindSim

Framework for Integration of Neuronal Data and SIgnaling Models. The associated paper is available 
at [https://doi.org/10.3389/fninf.2018.00038](https://doi.org/10.3389/fninf.2018.00038)

# About

The FindSim project maps models of neural and cellular signaling to 
experimental protocols and readouts. It runs the experiment on the model, and
provides a score that reports how closely the two match.

# LICENSE
This file and the files in this repository are licensed under GPL v3 or later.

# Version

Latest release is 1.1.0, which can be downloadable at  
	https://github.com/BhallaLab/FindSim/archive/v1.1.0.zip  
	https://github.com/BhallaLab/FindSim/archive/v1.1.0.tar.gz


# Install 
	To run FindSim script one needs to  
		- Install MOOSE which can be found here  
			https://moose.ncbs.res.in/readthedocs/install/install.html  
		- Install FindSim:  
			Clone the entire repository using  
  				>git clone https://github.com/BhallaLab/FindSim 
			or, clone specific branch such as "stable" using:
				>git clone -b <branch-name> https://github.com/BhallaLab/FindSim

=============================================================================
# File organization:
	FindSim/             				: project directory  
	FindSim/stable					: Stable branch. Stable version of `develop` branch  
	FindSim/Curated					: Folder contains FindSim worksheets to which the model is well fit.
	FindSim/models					: Model files 
	FindSim/findSim.py				: Main findSim script  
	FindSim/runAllParallel.py			: Batch/parallel wrapper script.  
	FindSim/FindSim-Exptworksheet.xlsx		: Template worksheet with inline help and units, for Microsoft Excel.  
	FindSim/FindSim-Exptworksheet.ods		: Template worksheet with inline help and units, for Libre Office.  
	FindSim/FindSim-Schema.xml 			: Schema for tsv files for worksheet.  
	FindSim/README.md				: This file  
						
=============================================================================
# Quick start: 
A. Run one of the example experiments on the default model, generating a graph to compare model to experiment:  
	To run the script, run the command in python and `synSynth7.g` is the latest model that is tested out the worksheets.  
  	>python findSim.py Curated/FindSim-Jain2009-Fig2B.tsv --model synSynth7.g  
  				or  
  	>python findSim.py Curated/FindSim-Jain2009-Fig2B.tsv  

B. Batch run:  
	-runAllParallel.py script runs the findSim program on all tsv files in the specified directory, computes their scores, and prints out basic stats of the scores. It can do this in parallel using Python's multiprocessing library.  
	
	>python runAllParallel.py Curated -n 8  (run of the entire set of `Curated` experiments on 8 cores)  
						or  
	>python runAllParallel.py Directory (of tsv files) -n (Number of processes to spawn) --model (synSynth7.g)  

C. Syntax help:  
	>python findSim.py -h  
	>python runAllParallel.py -h  


=============================================================================

Generating Figures for   
"FindSim: a Framework for Integrating Neuronal Data and Signaling Models."  
by  
Nisha A. Viswan, G.V. HarshaRani, Melanie I. Stefan, Upinder S. Bhalla
Front Neuroinform. 2018 Jun 26;12:38. doi: 10.3389/fninf.2018.00038. eCollection 2018.

All these are run using the development branch "stable"  
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
