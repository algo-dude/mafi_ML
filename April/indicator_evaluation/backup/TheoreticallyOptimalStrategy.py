import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode as m
from util import get_data

def author():
    return 'aladdha7'

def getprices(symbol, start_date, end_date):
    prices = get_data([symbol], pd.date_range(start_date, end_date))
    if 'SPY' not in symbol:
        prices.drop('SPY', axis=1, inplace=True)

    prices = prices.fillna(method='ffill')
    prices = prices.fillna(method='bfill')
    prices_normed = prices / prices.iloc[0]
    return prices_normed

def testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):

    prices = getprices(symbol, sd, ed)
    prices_temp = prices.copy()
    prices_temp['NextDay'] = prices_temp.shift(-1)
    trade_fwd = pd.DataFrame(index=prices.index)
    trade_bwd = pd.DataFrame(index=prices.index)

    # computing trades by looking at prices 1 day ahead
    trade_fwd['Order'] = np.where(prices_temp[symbol] < prices_temp['NextDay'], 'BUY', 'SELL')

    # Now looking at orders 1 day before and checking whether we opted for a Buy or Sell opp. If buy yesterday, then sell today and vice versa
    trade_bwd = trade_fwd.copy()
    trade_bwd['Order'] = trade_bwd.shift(1)

    trade_bwd = trade_bwd[1:]  # cant look prior to the first day
    trade_bwd['Orders_Temp'] = np.where(trade_bwd['Order'] == 'BUY', 'SELL', 'BUY')
    trade_bwd.drop(['Order'], axis=1, inplace=True)
    trade_bwd.columns = ['Order']

    trade_df = pd.concat([trade_fwd, trade_bwd])
    trade_df.sort_index(inplace=True, ascending=True)
    trade_df['Shares'] = 1000
    trade_df['Symbol'] = symbol
    trade_df = trade_df[['Order', 'Symbol', 'Shares']]

    return trade_df

def benchmark(symbol, sd, ed, shares):

    prices =  getprices(symbol, sd, ed)
    df_trades = pd.DataFrame(index = prices.index)
    df_trades['Order'], df_trades['Symbol'],df_trades['Shares'] = ['BUY',symbol, 0]

    start =df_trades.index.min()
    end = df_trades.index.max()
    df_trades.loc[start,:] = ['BUY', symbol, shares]
    df_trades.loc[end,:] = ['SELL', symbol, shares]
    return df_trades

def Portfolio_Statistics(portvals):
    daily_returns = portvals.copy()
    daily_returns[1:] = (portvals[1:] / portvals[:-1].values) - 1
    daily_returns = daily_returns[1:]

    cum_ret = (portvals[-1] / portvals[0]) - 1
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    sharpe_ratio = np.sqrt(252.0) * (avg_daily_ret / std_daily_ret)

    return cum_ret,avg_daily_ret,std_daily_ret,sharpe_ratio