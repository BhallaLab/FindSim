
class SimWrap():
    def __init__( self, *args, **kwargs ):
        self.ignoreMissingObj = kwargs["ignoreMissingObj"]
        self.modelLookup = {}
        self.modelId = ""
        self.plots = {} # Keys: Readout objects. Values: 2d numpy arrays
                
        return

    def _scaleParams( self, params ):
        if len(params) == 0:
            return
        if (len(params) % 3) != 0:
            raise SimError( "scaleParam: expecting triplets of [obj, field, scale], got: '{}'".format( params ) )
        for i in range( 0, len(params), 3):
            self._scaleOneParam( params[i:i+3] )
            # _scaleOneParam is a derived function

    def _scaleOneParam( self, params ): # place holder, to be overridden
        return

    def deleteItems( self, itemsToDelete ): # to be overridden
        return

    def subsetItems( self, modelSubset ): # to be overridden
        return

    def pruneDanglingObj( self, erSPlist ): # to be overridden
        return

    def changeParams( self, parameterChange ): # to be overridden
        return

    def loadModelFile( self, fname, modifyFunc, scaleParam, dumpFname, paramFname, tempModelLookup ): # to be overridden
        self.turnOffElec = True
        return

    def buildSolver( self, solver, useVclamp = False, turnOffElec = False ):
        return

    def buildVclamp( self, stim ):
        return

    def setHsolveState(self, state, pauseHsolve):
        return

    def makeReadoutPlots( self, readouts ):
        return

    def fillPlots( self, readout): # takes plots from sim and puts the numpy arrays of the plot values from sim into the Readout::plots field.
        return;
    
    def deliverStim( self, qe ):
        return

    def getCurrentTime( self ):
        return 0.0

    def advanceSimulation( self, advanceTime ):
        return

    def reinitSimulation( self ):
        return

    def sumFields( self, entityList, field ):
        return 0.0

    def getObjParam( self, entity, field ):
        return 0.0

    def steadyStateStims(self, stimList, responseList, isSeries = False, settleTime = 300 ):
        '''
        Computes steady_state output for specified stimulus combinatations.
        stimList is 2-D list of 
            (stimEntity, field, value, scale) tuples. 
        The first dimension is the combined stimulus for each data point
        The second dimension is the series of data points.
        responseList is list of 
            (respEntityList, field, refEntityList, field) 
        tuples for the readout. The respEntityList/refEntityList specify
        multiple entities whose values should be summed for the response.
        In some cases we have a special global reference stimulus. This
        is just another entry in the stimList.
        isSeries is true if the entries are successive, like a dose-response
        This function is used for a doser by having just the same
        stimulus entity throughout, for a series of doses.
        Returns the list of responses, and the list of matching references.
        '''
        return [], []
        
    def assignField( self, entity, field ):
        return

    def generateParamFile( self, model, fname ):
        return

    def deleteSimulation( self ):
        return

    def presettle( self ):
        return {}

    def assignPresettle( settledict ):
        return
