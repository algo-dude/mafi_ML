import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data
import indicators
import TheoreticallyOptimalStrategy as tos

def author():
    print ("dude, you are not the author of this code")


if __name__ == "__main__":
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = "JPM"

    #Calling indicator main function for generating indicator plots
    indicators.test_code_indicators(symbol, sd, ed)

    #Running testPolicy for TOS
    df_trades_optimal = tos.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=100000)

    #Running testPolicy for Benchmark Strategy
    df_trades_benchmark = tos.benchmark(symbol="JPM", sd=sd, ed=ed, shares=1000)

    # Comparing TOS vs Benchamrk Strategy
    tos.compare_tos_vs_benchmark(df_trades_optimal, df_trades_benchmark, symbol=symbol, sd=sd, ed=ed)