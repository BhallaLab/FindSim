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

# Install 

One can get `FindSim` using `python-pip`.

To install last stable release (__NOTE__ This uses moose version 3.1.4 (outdated
with this release))

     $ pip install FindSim 

Or, to install the nightly built,

     $ pip install FinSim --pre   # recommended 

Alternatively, you can download the source code and install it yourself.

1. Install MOOSE which can be found here https://moose.ncbs.res.in/readthedocs/install/install.html  
2. Install FindSim

```
git clone https://github.com/BhallaLab/FindSim
cd FindSim
python setup.py install  
```

After successful installation, two commands are available at your disposal
`findsim` and `findsim_parallel`. To see the help message, pass `-h` option to
either of these commands. For example, `findsim -h` will show you following
message.

```
usage: findsim [-h] [-m MODEL] [-d DUMP_SUBSET] [-p PARAM_FILE] [-t] [-hp]
               [-hs] [-o] [-s SCALE_PARAM SCALE_PARAM SCALE_PARAM]
               [-settle_time SETTLE_TIME]
               script

FindSim argument parser This program loads a kinetic model, and runs it with
the specified stimuli. The output is then compared with expected output
specified in the same file, to generate a model score.

positional arguments:
  script                Required: filename of experiment spec, in tsv format.

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Optional: model filename, .g or .xml
  -d DUMP_SUBSET, --dump_subset DUMP_SUBSET
                        Optional: dump selected subset of model into named
                        file
  -p PARAM_FILE, --param_file PARAM_FILE
                        Optional: Generate file of tweakable params belonging
                        to selected subset of model
  -t, --tabulate_output
                        Flag: Print table of plot values. Default is NOT to
                        print table
  -hp, --hide_plot      Hide plot output of simulation along with expected
                        values. Default is to show plot.
  -hs, --hide_subplots  Hide subplot output of simulation. By default the
                        graphs include dotted lines to indicate individual
                        quantities (e.g., states of a molecule) that are being
                        summed to give a total response. This flag turns off
                        just those dotted lines, while leaving the main plot
                        intact.
  -o, --optimize_elec   Optimize electrical computation. By default the
                        electrical computation runs for the entire duration of
                        the simulation. With this flag the system turns off
                        the electrical engine except during the times when
                        electrical stimuli are being given. This can be *much*
                        faster.
  -s SCALE_PARAM SCALE_PARAM SCALE_PARAM, --scale_param SCALE_PARAM SCALE_PARAM SCALE_PARAM
                        Scale specified object.field by ratio.
  -settle_time SETTLE_TIME, --settle_time SETTLE_TIME
                        Run model for specified settle time and return dict of
                        {path,conc}.
						
```

Command `findsim_parellel` is a helper utility: it runs multiple simulations
using `findsim` in parellel.

# Quick start

To run one of the example experiments on the default model (`synSynth7.g`) and generate a graph 
to compare model to experiment.  

```
findsim Curated/FindSim-Jain2009-Fig2B.tsv  
```

You can also pass the model explicitly, 

```
findsim Curated/FindSim-Jain2009-Fig2B.tsv --model models/synSynth7.g  
```


## Batch run

To findSim program on all tsv files in the specified directory, computes their
scores, and prints out basic stats of the scores, you should use
`findsim_parallel` command.
	
```
findsim_parellel Curated -n 8 
```

It will run the entire set of `Curated` experiments in parallel using 8
independant processes (it will be effectively if your computer has at least 8
cores). The value of `-n` should not be more than `N+1` where `N` is the number
of processors on your system (use system utility `nproc` to see this number).

More detailed invocation of this command looks like the following:

```
findsim_parallel path/to/tsv/files -n 6 --model synSynth7.g
```

# Repository organization

    FindSim/             		: project directory  
    FindSim/stable			: Stable branch. Stable version of `develop` branch  
    FindSim/Curated	   		: Folder contains FindSim worksheets to which the model is well fit.
    FindSim/models			: Model files 
    FindSim/findSim.py			: Main findSim script  
    FindSim/runAllParallel.py		: Batch/parallel wrapper script.  
    FindSim/FindSim-Exptworksheet.xlsx	: Template worksheet with inline help and units, for Microsoft Excel.  
    FindSim/FindSim-Exptworksheet.ods	: Template worksheet with inline help and units, for Libre Office.  
    FindSim/FindSim-Schema.xml 		: Schema for tsv files for worksheet.  
    FindSim/README.md			: This file  

# Extra

Generating Figures for  __FindSim: a Framework for Integrating Neuronal Data
and Signaling Models by  Nisha A. Viswan, G.V. HarshaRani, Melanie I. Stefan,
Upinder S. Bhalla Front Neuroinform. 2018 Jun 26;12:38. doi:
10.3389/fninf.2018.00038. eCollection 2018.__

All these are run using the branch `release.1.1.0`. Please change into the
branch to run these.

Figure 6: bottom  
    python findSim.py Curated/FindSim-Jain2009_Fig4F.tsv --model models/synSynth7.g  

Figure 7B:  
    python findSim.py Curated/FindSim-Bhalla1999_fig2B.tsv --model models/synSynth7.g  
    python findSim.py Curated/FindSim-Gu2004_Fig3.tsv --model models/synSynth7.g  

Figure 7C:  
    python findSim.py Curated/FindSim-Ji2010_fig1C_ERK_acute.tsv --model models/synSynth7.g  

Figure 7D:  
    python findSim.py Curated/FindSim-Bhalla1999_fig4C.tsv --model models/synSynth7.g  


# Other resources

- The web template for experiment worksheet can be found here
https://www.ncbs.res.in/faculty/bhalla-findsim/worksheet  

- The MOOSE site: http://moose.ncbs.res.in. MOOSE documentation:
  http://moose.ncbs.res.in/readthedocs/install/index_install.html

- Two papers were used as the initial basis for the models, and which in turn
  refer to a large number of experimental studies for their data:

    1. Bhalla US., Iyengar R. Emergent properties of networks of biological signaling pathways. Science. 1999 Jan 15;283(5400):381-7.  
    2. Jain P, and Bhalla, U.S. Signaling logic of activity-triggered dendritic protein synthesis: an mTOR gate but not a feedback switch. PLoS Comput Biol. 2009 Feb;5(2):e1000287. Epub 2009 Feb 13  

- Two more papers were used for some of the experiments

    1. Gu J, et al. Beta1,4-N-Acetylglucosaminyltransferase III down-regulates
       neurite outgrowth induced by costimulation of epidermal growth factor and
       integrins through the Ras/ERK signaling pathway in PC12 cells.
       Glycobiology. 2004 Feb;14(2):177-86. Epub 2003 Oct 23
    2. Ji Y, et al. Acute and gradual increases in BDNF concentration elicit
       distinct signaling and functions in neurons. Nat Neurosci. 2010
       Mar;13(3):302-9. doi: 10.1038/nn.2505. Epub 2010 Feb 21.

- DOQCS database, from which models were derived: http://doqcs.ncbs.res.in
  __Sivakumaran S. et al. The Database of Quantitative Cellular Signaling:
  management and analysis of chemical kinetic models of signaling networks.
  Bioinformatics. 2003. 19(3):408–415__
