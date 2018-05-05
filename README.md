# FindSim
Framework for Integration of Neuronal Data and SIgnaling Models.

The FindSim project maps models of neural and cellular signaling to 
experimental protocols and readouts. It runs the experiment on the model, and
provides a score that reports how closely the two match.

This file and the files in this repository are licensed under GPL v3 or later.

Quick start: 
A. Run one of the example experiments on the default model, generating a graph 
to compare model to experiment:

1. Install MOOSE
2. Install FindSim:
	git clone https://github.com/BhallaLab/FindSim
3. Navigate to release or to development branch, e.g.,
	cd ./FindSim/FindSim1.0.0
3. Run findSim on an example model:
	python findSim.py Curated/FindSim-Jain2009-Fig2B.tsv

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
python findSim.py FindSim-Jain2009_Fig4F.tsv

Figure 7B:
python findSim.py FindSim-Bhalla1999_fig2B.tsv

Figure 7C:
python findSim.py FindSim-Ji2010_fig1C_ERK_acute.tsv

Figure 7D:
python findSim.py FindSim-Bhalla1999_fig4C.tsv

=============================================================================

