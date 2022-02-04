


import numpy as np
from sklearn.tree import DecisionTreeRegressor


class DTLearner(object):
    '''
    Decision Tree Learner
    
    '''

    def __init__(self, leaf_size=1, verbose=False):
        '''
        Constructor
        '''
        self.tree=None
        self.leaf_size=leaf_size


    def author(self):
        '''
        Return:
            Return your name
        '''
        return "seth"

    def add_evidence(self, data_x, data_y):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """	  	   		  	  			  		 			     			  	 

        dataY=np.array([dataY])
        new_dataY=dataY.T	#transpose of dataY
        all_data=np.append(dataX,new_dataY,axis=1)
        self.tree=self.build_tree(all_data)

