import moose
import argparse
import simError
import simWrap
import simWrapMoose


class Modifier():
    def __init__(self, subset, sw ):
        self.subset = subset
        self.sw = sw

    def modifyFunc( self, erlist, modelWarning ):
        self.sw.subsetItems( self.subset )
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'input', type = str, help = "Name of input file with the MOOSE model. Can be either .g or .xml (SBML) format" )
    parser.add_argument( 'subset', type = str, nargs = '+', help = "Name(s) of subset pathway.")
    parser.add_argument( 'output', type = str, help = "Name of output file, either in .g or xml (SBML) format.")

    args = parser.parse_args()

    sw = simWrapMoose.SimWrapMoose( ignoreMissingObj = True, silent = False )
    mod = Modifier( args.subset, sw )
    sw.objMap = { i:[i] for i in args.subset }
    scaleParams = []
    paramFname = ""
    sw.loadModelFile( args.input, mod.modifyFunc, scaleParams, args.output, paramFname )

if __name__ == '__main__':
    main()
