import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data
from marketsimcode import compute_portvals
from indicators import getsma, getBBP, getMomentum


def Portfolio_Statistics(portvals):
    daily_returns = portvals.copy()
    daily_returns[1:] = (portvals[1:] / portvals[:-1].values) - 1
    daily_returns = daily_returns[1:]

    cum_ret = (portvals.iloc[-1] / portvals.iloc[0]) - 1
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    sharpe_ratio = np.sqrt(252.0) * (avg_daily_ret / std_daily_ret)

    return cum_ret,avg_daily_ret,std_daily_ret,sharpe_ratio


def benchmark(symbol, sd, ed, shares):
    prices = get_data([symbol], pd.date_range(sd, ed))
    if 'SPY' not in symbol:
        prices.drop('SPY', axis=1, inplace=True)

    prices = prices.fillna(method='ffill')
    prices = prices.fillna(method='bfill')
    prices = prices / prices.iloc[0]

    df_trades = pd.DataFrame(index=prices.index)
    df_trades[symbol] = 0

    start = df_trades.index.min()
    end = df_trades.index.max()
    df_trades.loc[start, symbol] = shares
    df_trades.loc[end, symbol] = -1 * shares
    return df_trades


def author():
    print ("aladdha7")

def testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
    signal = 0  # can be -1, 0, or 1, corresponding to a “short,” “out” or “long” position
    moving_window = 21
    prices = get_data([symbol], pd.date_range(sd, ed))

    if 'SPY' not in symbol:
        prices.drop('SPY', axis=1, inplace=True)
    prices = prices.fillna(method='ffill')
    prices = prices.fillna(method='bfill')
    prices = prices / prices.iloc[0, :]

    trades_df = pd.DataFrame(columns=['Order', 'Shares'], index=prices.index)

    sma, price_sma = getsma(prices, moving_window)

    upperband, lowerband, BBP = getBBP(prices, moving_window)
    momentum = getMomentum(prices, moving_window)


    for index in range(prices.shape[0]):
        i = prices.index[index]
        if signal == 0:

            if price_sma.loc[i, symbol] < 0.6 or BBP.loc[i, symbol] < 0.2 or momentum.loc[i, symbol] < -0.1:
                trades_df.loc[i] = ['BUY', 1000]

                signal = 1

            elif price_sma.loc[i, symbol] > 1.0 or BBP.loc[i, symbol] > 0.8 or momentum.loc[i, symbol] > 0.1:
                trades_df.loc[i] = ['SELL', 1000]
                signal = -1

        elif signal == -1:

            if price_sma.loc[i, symbol] < 0.6 or BBP.loc[i, symbol] < 0.2 or momentum.loc[i, symbol] < -0.1:
                trades_df.loc[i] = ['BUY', 2000]
                signal = 1

        elif signal == 1:
            if price_sma.loc[i, symbol] > 1.3 or BBP.loc[i, symbol] > 0.8 or momentum.loc[i, symbol] > 0.2:
                trades_df.loc[i] = ['SELL', 2000]
                signal = -1


    trades_df['Shares'] = np.where(trades_df['Order'] == 'BUY', trades_df['Shares'], -1 * trades_df['Shares'])
    trades_df = trades_df.loc[:, ['Shares']]
    trades_df.columns = [symbol]
    trades_df.fillna(0, inplace=True)

    return trades_df


def InSample() :
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    moving_window = 21

    # Manual Strategy
    df_trades_manual = testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv=100000)
    port_vals_manual = compute_portvals(df_trades_manual, start_val=100000, commission=9.95, impact=0.005)

    # Normalizing PortFolio Values
    port_vals_norm_manual = port_vals_manual / port_vals_manual.iloc[0]

    cum_ret_man, avg_daily_ret_man, std_daily_ret_man, sharpe_ratio_man = Portfolio_Statistics(port_vals_norm_manual)

    print()
    print(f"Date Range: {start_date} to {end_date} for {symbol}")
    print()
    print("Manual Strategy")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_man}")
    print(f"Cumulative Return of Fund: {cum_ret_man}")
    print(f"Standard Deviation of Fund: {std_daily_ret_man}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_man}")
    print(f"Final Portfolio Value: {port_vals_manual[-1]}")

    # Benchmark Strategy
    df_trades_benchmark = benchmark(symbol=symbol, sd=start_date, ed=end_date, shares=1000)
    port_vals_benchmark = compute_portvals(df_trades_benchmark, start_val=100000, commission=9.95, impact=0.005)

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
    print(f"Final Portfolio Value: {port_vals_benchmark[-1]}")



    fig, ax = plt.subplots(figsize=(15, 7.5))
    ax = port_vals_norm_manual.plot(color='red', label='Manual Strategy')
    port_vals_norm_benchmark.plot(ax=ax, color='green', label='Benchmark Strategy')

    for index, signal in df_trades_manual.iterrows():

        if df_trades_manual.loc[index, symbol] > 0:
            plt.axvline(x=index, color='b', linestyle='--', label='long')
        elif df_trades_manual.loc[index, symbol] < 0:
            plt.axvline(x=index, color='k', linestyle='--', label='short')

    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    plt.legend(handle_list, label_list)
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.title("Manual Strategy vs Benchmark - In Sample")
    plt.savefig('MS_InSample.png')

def OutOfSample() :
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    symbol = "JPM"
    moving_window = 21

    # Manual Strategy
    df_trades_manual = testPolicy(symbol= symbol, sd=start_date, ed=end_date, sv=100000)
    port_vals_manual = compute_portvals(df_trades_manual, start_val=100000, commission=9.95, impact=0.005)

    # Normalizing PortFolio Values
    port_vals_norm_manual = port_vals_manual / port_vals_manual.iloc[0]

    cum_ret_man, avg_daily_ret_man, std_daily_ret_man, sharpe_ratio_man = Portfolio_Statistics(port_vals_norm_manual)
    print()
    print(f"Date Range: {start_date} to {end_date} for {symbol}")
    print()
    print("Manual Strategy")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_man}")
    print(f"Cumulative Return of Fund: {cum_ret_man}")
    print(f"Standard Deviation of Fund: {std_daily_ret_man}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_man}")
    print(f"Final Portfolio Value: {port_vals_manual[-1]}")

    # Benchmark Strategy
    df_trades_benchmark = benchmark(symbol=symbol, sd=start_date, ed=end_date, shares=1000)
    port_vals_benchmark = compute_portvals(df_trades_benchmark, start_val=100000, commission=9.95, impact=0.005)

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
    print(f"Final Portfolio Value: {port_vals_benchmark[-1]}")

    fig, ax = plt.subplots(figsize=(15, 7.5))
    ax = port_vals_norm_manual.plot(color='red', label='Manual Strategy')
    port_vals_norm_benchmark.plot(ax=ax, color='green', label='Benchmark Strategy')

    for index, signal in df_trades_manual.iterrows():

        if df_trades_manual.loc[index, symbol] > 0:
            plt.axvline(x=index, color='b', linestyle='--', label='long')
        elif df_trades_manual.loc[index, symbol] < 0:
            plt.axvline(x=index, color='k', linestyle='--', label='short')

    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    plt.legend(handle_list, label_list)
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.title("Manual Strategy vs Benchmark - Out Sample")
    plt.savefig('MS_OutSample.png')


if __name__ == "__main__":
    InSample()
    OutOfSample()