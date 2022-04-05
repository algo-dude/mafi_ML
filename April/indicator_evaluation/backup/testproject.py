import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data
import marketsimcode as marketsim
import indicators

import TheoreticallyOptimalStrategy as tos

def author():
    print ("aladdha7")

def test_code_indicators(symbol = "JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):

    moving_window = 14
    prices = indicators.getprices([symbol], sd, ed)

    # plotting SMA
    sma, sma_by_price, sma_50_days = indicators.getsma(prices, moving_window)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Simple Moving Average")
    ax.plot(prices, "goldenrod", label="Normalized Price")
    ax.plot(sma, "magenta", label="SMA")
    ax.legend(loc="best")
    fig.savefig('Indicator1_SMA.png')
    plt.close()

    # plotting short term SMA vs Long term SMA
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Cross Over Simple Moving Average")
    ax.plot(prices, "goldenrod", label="Normalized Price")
    ax.plot(sma, "magenta", label=f"SMA {moving_window} days")
    plt.plot(sma_50_days, 'gray', label='SMA 50 days')
    ax.legend(loc="best")
    fig.savefig('Indicator1_crossover_SMA.png')
    plt.close()

    # plotting Bollinger Bands
    upperband, lowerband, BBP = indicators.getBBP(prices, moving_window)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Bollinger Bands")
    ax.plot(prices, "goldenrod", label='Normalized Price')
    ax.plot(sma, "magenta", label="Rolling Average")
    ax.plot(upperband, "slateblue", label="Upper Band")
    ax.plot(lowerband, "deepskyblue", label="Lower Band")
    ax.legend()
    fig.savefig('Indicator2_BB.png')
    plt.close()

    # plotting Bollinger Band Percentage
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Bollinger Bands Percentage")
    ax.plot(prices, "goldenrod", label='Normalized Price')
    ax.plot(BBP, "gray", label='BBP%')
    ax.legend()
    fig.savefig('Indicator2_BBP.png')
    plt.close()

    # plotting Momentum
    momentum = indicators.getMomentum(prices, moving_window)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Momentum")
    ax.plot(prices, "goldenrod", label='Normalized Price')
    ax.plot(momentum, "blue", label="Momentum")
    ax.legend()
    fig.savefig('Indicator3_Momentum.png')
    plt.close()

    # plotting Volatility
    volatility = indicators.getVolatility(prices, moving_window)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Volatility")
    ax.plot(prices, "goldenrod", label='Normalized Price')
    ax.plot(volatility, label="Volatility")
    ax.legend()
    fig.savefig('Indicator4_Volatility.png')
    plt.close()

    # plotting MACD
    MACD, signal = indicators.getMACD(prices)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="MACD")
    ax.plot(MACD, "gray", label='MACD')
    ax.plot(signal, "coral", label="MACD Signal")
    ax.legend()
    fig.savefig('Indicator5_MACD.png')
    plt.close()

def test_code_strategy(symbol = "JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):

    # Theoretically Optimal Strategy
    df_trades_optimal = tos.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=100000)
    port_vals_optimal = marketsim.compute_portvals(df_trades_optimal, start_val=100000, commission=0, impact=0)

    # Normalizing PortFolio Values
    port_vals_norm_optimal = port_vals_optimal / port_vals_optimal.iloc[0]
    cum_ret_opt, avg_daily_ret_opt, std_daily_ret_opt, sharpe_ratio_opt = tos.Portfolio_Statistics(port_vals_norm_optimal)

    print(f"Date Range: {sd} to {ed} for {symbol}")
    print()
    print("Optimal Strategy")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_opt}")
    print(f"Cumulative Return of Fund: {cum_ret_opt}")
    print(f"Standard Deviation of Fund: {std_daily_ret_opt}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_opt}")
    print(f"Final Portfolio Value: {port_vals_optimal[-1]}")

    # Benchmark Strategy
    df_trades_benchmark = tos.benchmark(symbol="JPM", sd=sd, ed=ed, shares=1000)
    port_vals_benchmark = marketsim.compute_portvals(df_trades_benchmark, start_val=100000, commission=0, impact=0)

    # Normalizing PortFolio Values
    port_vals_norm_benchmark = port_vals_benchmark / port_vals_benchmark.iloc[0]

    cum_ret_bench, avg_daily_ret_bench, std_daily_ret_bench, sharpe_ratio_bench = tos.Portfolio_Statistics(
        port_vals_norm_benchmark)
    print()
    print("Benchmark Strategy")

    print(f"Sharpe Ratio of Fund: {sharpe_ratio_bench}")
    print(f"Cumulative Return of Fund: {cum_ret_bench}")
    print(f"Standard Deviation of Fund: {std_daily_ret_bench}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_bench}")
    print(f"Final Portfolio Value: {port_vals_benchmark[-1]}")

    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Date', ylabel="Normalized Portfolio Value", title="Theoretically Optimal Strategy vs Benchmark Strategy")
    ax.plot(port_vals_norm_optimal, "magenta", label='Optimal Strategy')
    ax.plot(port_vals_norm_benchmark, "dodgerblue", label="Benchmark Strategy")
    ax.legend()
    fig.savefig('Experiment2.png')
    plt.close()

if __name__ == "__main__":
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    test_code_indicators(symbol, sd, ed)
    test_code_strategy(symbol, sd, ed)