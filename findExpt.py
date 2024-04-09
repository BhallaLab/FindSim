'''
findExpt.py: Finds a list of experiments from the provided directory,
looking for those which use entities from the provided mapfile.
'''
import os
from subprocess import call
import json
import argparse
import findSim

experiment_model = {}
model_experiment = {}

# Kumar has a settle time of much more than 5000 sec.
# Emery has a settle time of much more than 5000 sec.
excludeList = [
        'Kumar2005_Fig6L_pAKT.json','Emery2012_Fig1C.json',
    ]

def main():
    ''' 
    This program loads a map file and then goes through a directory
    of experiments to run on the model(s) associated with the map file.
    It picks out those experiments whose inputs and outputs are present
    in the map file.
    '''
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument( "mapFile", type=str, help = "Required: name of findSim mapfile to use for all entity names in experiment" )
    parser.add_argument( "-e", "--exptDir", type = str, 
        help = "Optional: Directory in which to look for all experiments to check.", default = "HTPipeline/Expts" )
    args = parser.parse_args()

    #directory = '/home/bhalla/homework/Nishaa/2022/HTPipeline/Expts'
    listOfFiles = [f for f in os.listdir(args.exptDir) if os.path.isfile(os.path.join(args.exptDir, f) )]

    if len( listOfFiles ) == 0:
        print( "Warning: No experiment files found in ", args.exptDir )
        return

    mapFile = args.mapFile
    exptList = []

    with open(mapFile, "r") as json_file:
        mapFilename = os.path.basename(mapFile)
        jsonMap = json_file.read()
        data = json.loads(jsonMap)

        for filename in listOfFiles:
            if filename.endswith(".json"):
                filepath = os.path.join( args.exptDir, filename )
                if filename not in excludeList:
                    experiment, stims, readouts, modelx1 = findSim.loadJson( filepath,mapFile)
                    #print(filename,experiment.exptType)
                    stimuliFound = True
                    readoutFound = True

                    if experiment.exptType.lower() != 'directparameter':
                        stimulusEntities = [ st.entities[0] for st in stims]
                        #print( "RE = ", readouts.entities )
                        readoutEntities = readouts.entities
                        readoutFound = (readoutEntities[0] in data.keys())
                        for st in stimulusEntities:
                            if st not in  data.keys():
                                stimuliFound = False
                        if readoutFound and stimuliFound:
                            exptList.append( (filename, st, readoutEntities[0] ) )
                            if mapFilename not in model_experiment:
                                model_experiment[mapFilename]=[filename]
                            else:
                                model_experiment[mapFilename].append(filename)

                            if filename not in experiment_model:
                                experiment_model[filename]=[mapFilename]

                            else:
                                experiment_model[filename].append(mapFilename)

                        #print("s and r ",mapFilename,":",filename,":",experiment.exptType,":",stimuli_entities,":",readout_entities,":",stimuli_found,":",readout_found)
                        continue
                    else:
                        readoutEntities = []
                        for rd in readouts.directParamData:
                            re = rd['entity']
                            readoutEntities.append(re)
                            if re in data.keys():
                                exptList.append( (filename, "none", re ) )

                        for rd in readoutEntities:
                            if rd not in data.keys():
                                readoutFound = False
                        if readoutFound:
                            if mapFilename not in model_experiment:
                                model_experiment[mapFilename]=[filename]
                            else:
                                model_experiment[mapFilename].append(filename)
                                
                            if filename not in experiment_model:
                                experiment_model[filename]=[mapFilename]
                            else:
                                experiment_model[filename].append(mapFilename)
                        #print("s and r ",mapFilename,":",filename,":",experiment.exptType,":",stimuli_entities,":",readout_entities,":",'-',":",readout_found)

    exptList = sorted( list( set( exptList ) ), key = lambda x: x[0] )
    print( "    {:40s}{:18s}{:18}".format( "ExptFilename", "Stim", "Readout" ))
    print( "    {0:40s}{0:18s}{0:18s}".format( "------------------" ) )
    for idx, (f, s, r) in enumerate( exptList ):
        print( "{:<4d}{:40s}{:18s}{:18s}".format( idx, f, s, r ) )
'''
    for k,v in model_experiment.items():
        print("\n",k ,":\n", v)
'''


if __name__ == "__main__":
    main()
