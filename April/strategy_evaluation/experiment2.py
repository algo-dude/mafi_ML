import datetime as dt
import random
import pandas as pd
import numpy as np
import util as ut
import matplotlib.pyplot as plt
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

def test_code():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    moving_window = 21

    # Strategy Learner

    # Imapct 0.0
    learner = sl.StrategyLearner(verbose=False, impact=0.0)
    learner.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)
    df_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    port_vals = compute_portvals(df_trades, start_val=100000, commission=0.0, impact=0.0)
    port_vals_norm = port_vals / port_vals.iloc[0]

    # Imapct 0.002
    learner1 = sl.StrategyLearner(verbose=False, impact=0.002)
    learner1.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)
    df_trades1 = learner1.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    port_vals1 = compute_portvals(df_trades1, start_val=100000, commission=0.0, impact=0.002)
    port_vals_norm1 = port_vals1 / port_vals1.iloc[0]

    # Imapct 0.05
    learner2 = sl.StrategyLearner(verbose=False, impact=0.05)
    learner2.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)
    df_trades2 = learner2.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    port_vals2 = compute_portvals(df_trades2, start_val=100000, commission=0.0, impact=0.05)
    port_vals_norm2 = port_vals2 / port_vals2.iloc[0]

    # Imapct 0.1
    learner3 = sl.StrategyLearner(verbose=False, impact=0.1)
    learner3.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)
    df_trades3 = learner3.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    port_vals3 = compute_portvals(df_trades3, start_val=100000, commission=0.0, impact=0.1)
    port_vals_norm3 = port_vals3 / port_vals3.iloc[0]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax = port_vals_norm.plot( label='Impact 0.0')
    port_vals_norm1.plot(ax=ax,  label='Impact 0.002')
    port_vals_norm2.plot(ax=ax, label='Impact 0.05')
    port_vals_norm3.plot(ax=ax, label='Impact 0.1')

    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.title("Strategy Learner with different impact values")
    plt.savefig("Experiment2.png")

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = Portfolio_Statistics(port_vals_norm)
    print(f"Date Range: {sd} to {ed} for {symbol}")
    print()
    print("Strategy Learner with Impact 0.0")
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Cumulative Return of Fund: {cum_ret}")
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")

    cum_ret1, avg_daily_ret1, std_daily_ret1, sharpe_ratio1 = Portfolio_Statistics(port_vals_norm1)

    print()
    print("Strategy Learner with Impact 0.002")
    print(f"Average Daily Return of Fund: {avg_daily_ret1}")
    print(f"Cumulative Return of Fund: {cum_ret1}")
    print(f"Standard Deviation of Fund: {std_daily_ret1}")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio1}")

    cum_ret2, avg_daily_ret2, std_daily_ret2, sharpe_ratio2 = Portfolio_Statistics(port_vals_norm2)

    print()
    print("Strategy Learner with Impact 0.05")
    print(f"Average Daily Return of Fund: {avg_daily_ret2}")
    print(f"Cumulative Return of Fund: {cum_ret2}")
    print(f"Standard Deviation of Fund: {std_daily_ret2}")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio2}")

    cum_ret3, avg_daily_ret3, std_daily_ret3, sharpe_ratio3 = Portfolio_Statistics(port_vals_norm3)

    print()
    print("Strategy Learner with Impact 0.1")
    print(f"Average Daily Return of Fund: {avg_daily_ret3}")
    print(f"Cumulative Return of Fund: {cum_ret3}")
    print(f"Standard Deviation of Fund: {std_daily_ret3}")
    print(f"Sharpe Ratio of Fund: {sharpe_ratio3}")

    print()
    print("Number of trades with impact 0.0 is", df_trades[df_trades != 0].count()[0])
    print("Number of trades with impact 0.002 is", df_trades1[df_trades1 != 0].count()[0])
    print("Number of trades with impact 0.05 is", df_trades2[df_trades2 != 0].count()[0])
    print("Number of trades with impact 0.1 is", df_trades3[df_trades3 != 0].count()[0])


if __name__ == "__main__":

    np.random.seed(123456)
    test_code()