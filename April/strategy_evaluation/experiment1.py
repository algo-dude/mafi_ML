import datetime as dt
import random
import pandas as pd
import numpy as np
import util as ut
import matplotlib.pyplot as plt
import ManualStrategy as ms
import StrategyLearner as sl
from marketsimcode import compute_portvals


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
    prices = ut.get_data([symbol], pd.date_range(sd, ed))
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


def InSample():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    moving_window = 21

    # Benchmark Strategy
    df_trades_benchmark = benchmark(symbol= symbol , sd=sd, ed=ed, shares=1000)
    port_vals_benchmark = compute_portvals(df_trades_benchmark, start_val=100000, commission=9.95, impact=0.005)

    # Normalizing PortFolio Values
    port_vals_norm_benchmark = port_vals_benchmark / port_vals_benchmark.iloc[0]

    cum_ret_bench, avg_daily_ret_bench, std_daily_ret_bench, sharpe_ratio_bench = Portfolio_Statistics(
        port_vals_norm_benchmark)

    print(f"Date Range: {sd} to {ed} for {symbol}")
    print()
    print("Benchmark Strategy")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_bench}")
    print(f"Cumulative Return of Fund: {cum_ret_bench}")
    print(f"Standard Deviation of Fund: {std_daily_ret_bench}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_bench}")
    print(f"Final Portfolio Value: {port_vals_benchmark[-1]}")

    # Manual Strategy
    df_trades_manual = ms.testPolicy(symbol= symbol, sd=sd, ed=ed, sv=100000)
    port_vals_ms = compute_portvals(df_trades_manual, start_val=100000, commission=9.95, impact=0.005)

    # Normalizing PortFolio Values
    port_vals_norm_ms = port_vals_ms / port_vals_ms.iloc[0]

    cum_ret_ms, avg_daily_ret_ms, std_daily_ret_ms, sharpe_ratio_ms = Portfolio_Statistics(port_vals_norm_ms)

    print()
    print("Manual Strategy")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_ms}")
    print(f"Cumulative Return of Fund: {cum_ret_ms}")
    print(f"Standard Deviation of Fund: {std_daily_ret_ms}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_ms}")
    print(f"Final Portfolio Value: {port_vals_ms[-1]}")

    # Strategy Learner

    learner = sl.StrategyLearner(verbose=False, impact=0.005)
    learner.add_evidence(symbol= symbol, sd=sd, ed=ed, sv=100000)
    df_trades_strategy = learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=100000)

    port_vals_sl = compute_portvals(df_trades_strategy, start_val=100000, commission=9.95, impact=0.005)

    # Normalizing PortFolio Values
    port_vals_norm_sl = port_vals_sl / port_vals_sl.iloc[0]

    cum_ret_sl, avg_daily_ret_sl, std_daily_ret_sl, sharpe_ratio_sl = Portfolio_Statistics(port_vals_norm_sl)

    print()
    print("Strategy Learner")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio_sl}")
    print(f"Cumulative Return of Fund: {cum_ret_sl}")
    print(f"Standard Deviation of Fund: {std_daily_ret_sl}")
    print(f"Average Daily Return of Fund: {avg_daily_ret_sl}")
    print(f"Final Portfolio Value: {port_vals_sl[-1]}")

    fig, ax = plt.subplots(figsize=(12, 7))
    ax = port_vals_norm_ms.plot(color='red', label='Manual Strategy')
    port_vals_norm_benchmark.plot(ax=ax, color='green', label='Benchmark Strategy')
    port_vals_norm_sl.plot(ax=ax, color='blue', label='Strategy Learner')

    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.title("Exp 1 - In sample with Commisision 9.95 & impact 0.005")

    plt.savefig('Exp1_InSample.png')


if __name__ == "__main__":

    np.random.seed(123456)

    InSample()