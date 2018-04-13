# FindSim
Framework for Integration of Neuronal Data and SIgnaling Models.

The template for experiment worksheet can be found here https://docs.google.com/spreadsheets/d/13J5jZD461OZjtJgsnXYnuXN7MRo9VQPE6JM3kbfrpIs/edit?usp=sharing

To run FindSim script one needs to install moose which can be found here
https://moose.ncbs.res.in/readthedocs/install/install/install.html

To clone the FindSim repository use
  git clone https://github.com/BhallaLab/FindSim 
This will create folder called "FindSim" which contains
FindSim script, model files and Curated and NonCurated folder where experimental worksheets are stored.
`Curated` folder contains the FindSim worksheet which is tested again the model.
 `Non-Curated` worksheet which are yet to test.
 
 To run the script one need to run the command in python
 >python findSim.py experiment_worksheet.tsv --model (model filename) --hide_plot

runAllParallel.py script runs the findSim program on all tsv files in the specified directory, computes their scores, and prints out basic stats of the scores. It can do this in parallel using Python's multiprocessing library.

>python runAllParallel.py Directory (of tsv files) -n (Number of processes to spawn)

