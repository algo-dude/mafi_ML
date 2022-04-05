import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode as marketsim
from util import get_data

def author():
    return 'these are not the droids you are looking for'

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

    #Looking 1 day ahead
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
    trade_df['Shares'] = np.where(trade_df['Order'] =='BUY', 1000, -1000)
    trade_df = trade_df.loc[:, ['Shares']]
    trade_df.columns = [symbol]

    return trade_df

def benchmark(symbol, sd, ed, shares):

    prices =  getprices(symbol, sd, ed)
    df_trades = pd.DataFrame(index = prices.index)
    df_trades[symbol] = 0

    start =df_trades.index.min()
    end = df_trades.index.max()
    df_trades.loc[start,symbol] = shares
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

def compare_tos_vs_benchmark(df_trades_optimal, df_trades_benchmark, symbol = "JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):

    #Theoretically Optimal Strategy
    port_vals_optimal = marketsim.compute_portvals(df_trades_optimal, start_val=100000, commission=0, impact=0)

    # Normalizing PortFolio Values
    port_vals_norm_optimal = port_vals_optimal / port_vals_optimal.iloc[0]
    cum_ret_opt, avg_daily_ret_opt, std_daily_ret_opt, sharpe_ratio_opt = Portfolio_Statistics(
        port_vals_norm_optimal)

    print(f"Date Range: {sd} to {ed} for {symbol}")
    print()
    print("Optimal Strategy")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_opt}")
    print(f"Cumulative Return of Fund: {cum_ret_opt}")
    print(f"Standard Deviation of Fund: {std_daily_ret_opt}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_opt}")


    #Benchmark Strategy
    port_vals_benchmark = marketsim.compute_portvals(df_trades_benchmark, start_val=100000, commission=0, impact=0)

    # Normalizing PortFolio Values
    port_vals_norm_benchmark = port_vals_benchmark / port_vals_benchmark.iloc[0]

    cum_ret_bench, avg_daily_ret_bench, std_daily_ret_bench, sharpe_ratio_bench = Portfolio_Statistics(
        port_vals_norm_benchmark)
    print()
    print("Benchmark Strategy")

    print(f"Sharpe Ratio of Fund: {sharpe_ratio_bench}")
    print(f"Cumulative Return of Fund: {cum_ret_bench}")
    print(f"Standard Deviation of Fund: {std_daily_ret_bench}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_bench}")

    #TOS vs Benchamrk Strategy Plot
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Date', ylabel="Normalized Portfolio Value",
           title="Theoretically Optimal Strategy vs Benchmark Strategy")
    ax.plot(port_vals_norm_optimal, "red", label='Optimal Strategy')
    ax.plot(port_vals_norm_benchmark, "green", label="Benchmark Strategy")
    ax.legend()
    fig.savefig('Experiment2.png')
    plt.close()

