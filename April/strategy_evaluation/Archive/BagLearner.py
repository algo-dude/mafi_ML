import RTLearner as rt
import numpy as np
from scipy import stats

class BagLearner(object):

    def __init__(self, learner = rt.RTLearner, kwargs = {'leaf_size': 1}, bags = 20, boost = False, verbose = False):
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(0, bags):
            self.learners.append(learner(**self.kwargs))

    def author(self):
        return 'aladdha7'

    def add_evidence(self, xTrain, yTrain):

        for x in range(0, self.bags):
            bagIndices = np.random.choice(xTrain.shape[0], xTrain.shape[0])
            xBag = xTrain[bagIndices]
            yBag = yTrain[bagIndices]
            self.learners[x].add_evidence(xBag, yBag)

    def query(self, xTest):
        predictions = []
        for x in range(0, self.bags):
            pred = self.learners[x].query(xTest)
            predictions.append(pred)

        predictions = np.asarray(predictions)
        predictions = stats.mode(predictions, axis=0)
        predictions = predictions[0]
        return predictions