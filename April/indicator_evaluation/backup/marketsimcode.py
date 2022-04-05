		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
import datetime as dt  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
import os  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
import numpy as np 		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
import pandas as pd  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
from util import get_data, plot_data  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
def compute_portvals(  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    orders,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    start_val=1000000,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    commission=9.95,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    impact=0.005,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
):
    orders = orders
    orders.sort_index(inplace=True)

    start_date = orders.index.min()
    end_date = orders.index.max()
    stocks = list(orders.Symbol.unique())

   #Getting Stock Prices for the range start_date - end_date
    prices = get_data(stocks, pd.date_range(start_date, end_date))
    prices.ffill(inplace=True)    #Forward Filling first
    prices.bfill(inplace=True)    #Backward filling

    #SPY gets automatically added using get_data. So, delete SPY if not in the list of orders
    if 'SPY' not in stocks:
        prices.drop('SPY', axis=1, inplace=True)

    prices['Cash'] = 1   #Adding a cash field to prices and initializing to 1 so that we can multiply it straight away with holdings

    trade = pd.DataFrame(np.zeros(prices.shape), columns=prices.columns, index=prices.index)
    trade.iloc[0, -1] = start_val  #Cash for first date set to start value

    for index, row in orders.iterrows():
        stock = row['Symbol']
        order_type = row['Order']
        shares = row['Shares']
        stock_price = prices.loc[index, stock]  # getting stock price from prices df

        if order_type == 'SELL':
            multiplier = -1
            trade.loc[index, stock] = trade.loc[index, stock] - shares
            stock_price = stock_price - (stock_price * impact)

        else:
            multiplier = 1
            trade.loc[index, stock] = trade.loc[index, stock] + shares
            stock_price = stock_price + (stock_price * impact)

        # accounting market impact
        trade.loc[index, 'Cash'] = trade.loc[index, 'Cash'] - commission - (stock_price * shares * multiplier)

    holding = trade.cumsum()
    holding_value = holding * prices  # computing stock total values
    portvals = holding_value.sum(axis=1)

    return portvals


