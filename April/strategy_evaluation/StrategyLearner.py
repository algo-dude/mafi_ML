""""""  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
"""  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
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
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
import datetime as dt  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
import random
import pandas as pd
import numpy as np
import util as ut
import BagLearner as bl
import RTLearner as rt
from indicators import getsma, getBBP, getMomentum

class StrategyLearner(object):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			

    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Constructor method  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 5}, bags=25, boost=False,
                                     verbose=False)

    def author():
        print("aladdha7")


    def add_evidence(self, symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=10000):

        moving_window = 21

        prices = ut.get_data([symbol], pd.date_range(sd, ed))

        if 'SPY' not in symbol:
            prices.drop('SPY', axis=1, inplace=True)
        prices = prices.fillna(method='ffill')
        prices = prices.fillna(method='bfill')
        prices = prices / prices.iloc[0, :]

        # Getting Indicators values
        sma, price_sma = getsma(prices, moving_window)
        upperband, lowerband, BBP = getBBP(prices, moving_window)
        momentum = getMomentum(prices, moving_window)

        # Storing all the indicator values in a dataframe
        indicators_df = pd.concat((sma, BBP, momentum), axis=1)
        indicators_df.columns = ['SMA', 'BBP', 'Momentum']
        indicators_df.fillna(0, inplace=True)

        # Creating Xtrain, Ytrain

        days = 10   #N day return
        Xtrain = indicators_df[:-days].values  # This will be same as our indicator values.

        # Constructing trainY
        Ytrain = np.zeros(Xtrain.shape[0])  # This will be based on N day Future return

        YBUY = (0.015 + self.impact)
        YSELL = (-0.015 - self.impact)

        for i in range(prices.shape[0] - days):

            ret = (prices.loc[prices.index[i + 10], symbol] / prices.loc[prices.index[i], symbol]) - 1.0

            if ret > YBUY:
                Ytrain[i] = 1  # LONG

            elif ret < YSELL:
                Ytrain[i] = -1  # SHORT

            else:
                Ytrain[i] = 0  # CASH

        # Training the learner
        self.learner.add_evidence(Xtrain, Ytrain)

    def testPolicy(self, symbol="IBM", sd=dt.datetime(2009, 1, 1), ed=dt.datetime(2010, 1, 1), sv=10000):
        moving_window = 21

        prices = ut.get_data([symbol], pd.date_range(sd, ed))

        if 'SPY' not in symbol:
                prices.drop('SPY', axis = 1, inplace = True)
        prices= prices.fillna(method ='ffill')
        prices = prices.fillna(method = 'bfill')
        prices = prices/prices.iloc[0,:]

        sma, price_sma = getsma(prices, moving_window)
        upperband, lowerband, BBP = getBBP(prices, moving_window)
        momentum = getMomentum(prices, moving_window)

        indicators_df = pd.concat((sma,BBP,momentum),axis=1)
        indicators_df.columns = ['SMA','BBP', 'Momentum']
        indicators_df.fillna(0, inplace = True)

        Xtest = indicators_df.values

        # Querying the learner
        Ytest = self.learner.query(Xtest)
        #print(Ytest)

        # Creating the trades DataFrame
        trades_df = prices.copy()
        trades_df.loc[:] = 0

        signal = 0  #Buy, Sell or Hold

        for i in range(prices.shape[0]-1):

            index = prices.index[i]

            if signal == 0:

                if Ytest[0][i] > 0 :
                    trades_df.loc[index, :] = 1000
                    signal = 1

                elif Ytest[0][i] < 0 :
                    trades_df.loc[index, :] = -1000
                    signal = -1

            elif signal == -1:
                if Ytest[0][i] > 0 :
                    trades_df.loc[index,:] = 2000
                    signal = 1

            elif signal == 1:
                if Ytest[0][i] < 0:
                    trades_df.loc[index,:] = - 2000
                    signal = -1

        return trades_df


if __name__ == "__main__":  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    print("One does not simply think up a strategy")  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
