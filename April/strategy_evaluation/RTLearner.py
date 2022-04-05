""""""
"""  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			

Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
Atlanta, Georgia 30332  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
All Rights Reserved  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			

Template code for CS 4646/7646  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			

Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
works, including solutions to the projects assigned in this course. Students  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
and other users of this template code are advised not to share it with others  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
or to make it available on publicly viewable websites including repositories  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
or edited.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			

We do grant permission to share solutions privately with non-students such  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
as potential employers. However, sharing with other current or future  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
GT honor code violation.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			

-----do not edit anything above this line---  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
"""

import numpy as np

class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):

        """
        Constructor method

        """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None

    def author(self):
        return 'aladdha7'  # replace tb34 with your Georgia Tech username

    def add_evidence(self, Xtrain, Ytrain):
        self.tree = self.build_tree(Xtrain, Ytrain)
        return self.tree

    def build_tree(self, Xtrain, Ytrain):
        # Identifying the leaf nodes

        if Ytrain.shape[0] <= self.leaf_size:  # if #of nodes left < leaf_size
            return (np.array([[-1, np.mean(Ytrain), np.nan, np.nan]]))

        if (np.all(Ytrain == Ytrain[0])):  # if all values are the same
            return (np.array([[-1, np.mean(Ytrain), np.nan, np.nan]]))

        # randomly picking the feature to split on from Xtrain
        best_feature_index = np.random.randint(0, Xtrain.shape[1])
        split_val = np.median(Xtrain[:, best_feature_index])  # Best feature split value

        # when the leraner is not able to split the feature, return leaf, # Ed edge case
        if (Xtrain[Xtrain[:, best_feature_index] <= split_val]).shape[0] == Xtrain.shape[0]:    #when all values are in left tree
            return np.array([[-1, np.mean(Ytrain), np.nan, np.nan]])

        if (Xtrain[Xtrain[:, best_feature_index] > split_val]).shape[0] == Xtrain.shape[0]:        #when all values are in right tree
            return np.array([[-1, np.mean(Ytrain), np.nan, np.nan]])

        left_tree = self.build_tree(Xtrain[Xtrain[:, best_feature_index] <= split_val], Ytrain[Xtrain[:, best_feature_index] <= split_val])
        right_tree = self.build_tree(Xtrain[Xtrain[:, best_feature_index] > split_val], Ytrain[Xtrain[:, best_feature_index] > split_val])

        root = np.array([[best_feature_index, split_val, 1, left_tree.shape[0] + 1]])
        return (np.vstack((root, left_tree, right_tree)))

    def query(self, Xtest):

        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        Ypred = np.zeros(shape=(Xtest.shape[0],))  # initialising a numpy array of same shape as number of points
        i = 0
        for row in Xtest:
            current_node_index = 0
            node = self.tree[current_node_index]  # getting the node value in the form [feature, split_val, left, right]
            while node[0] != -1:  # checking if it is a leaf (val = -1)
                colIndex = int(node[0])

                if row[colIndex] <= node[1]:
                    current_node_index += int(node[2])  # Left index at node column 3 (index = 2)
                    node = self.tree[current_node_index]
                else:
                    current_node_index += int(node[3])  # Right index at node column 4 (index = 3)
                    node = self.tree[current_node_index]
            Ypred[i] = (node[1])  # if leaf, then return the leaf value (same as start_val in case of leaf)
            i = i + 1
        return Ypred


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")