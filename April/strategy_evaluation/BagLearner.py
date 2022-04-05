import RTLearner as rt
import numpy as np
from scipy import stats

class BagLearner(object):

    def __init__(self, learner = rt.RTLearner, kwargs = {'leaf_size': 1}, bags = 20, boost = False, verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(self.bags):
            self.learners.append(learner(**self.kwargs))


    def add_evidence(self,  Xtrain, Ytrain):

        for i in range(self.bags):
            #bagIndices = np.random.choice(xTrain.shape[0], xTrain.shape[0])
            index = np.random.choice(Ytrain.shape[0], size=Ytrain.shape[0], replace=True)
            data_bagX = Xtrain[index]
            data_bagY = Ytrain[index]
            #xBag = xTrain[bagIndices]
            #yBag = yTrain[bagIndices]
            #self.learners[x].add_evidence(xBag, yBag)

            self.learners[i].add_evidence(data_bagX, data_bagY)

    def query(self, Xtest):

        Ypred = np.ones([self.bags, Xtest.shape[0]])
        for i in range(self.bags):
            Ypred[i] = self.learners[i].query(Xtest)
        Ypred_mode = stats.mode(Ypred, axis=0)[0]
        return Ypred_mode

    if __name__ == "__main__":
        print("the secret clue is 'zzyzx'")


