import pandas as pd
import numpy as np
import yfinance as yf
from ta.volatility import average_true_range as atr

SPX = yf.download('^GSPC', start='1990-01-01', end='2018-01-01')
RUA = yf.download('^RUA', start='1990-01-01', end='2018-01-01')
# price is already adjusted
SPX = SPX.drop(['Adj Close'], axis=1)
RUA = RUA.drop(['Adj Close'], axis=1)
# 10/200 MA
SPX['MA200'] = SPX['Close'].rolling(window=200).mean()
RUA['MA200'] = RUA['Close'].rolling(window=200).mean()
SPX['MA10'] = SPX['Close'].rolling(window=10).mean()
RUA['MA10'] = RUA['Close'].rolling(window=10).mean()
# ATR 10 for volatility
SPX['ATR10'] = atr(high=SPX['High'], low=SPX['Low'], close=SPX['Close'], window=10)
RUA['ATR10'] = atr(high=RUA['High'], low=RUA['Low'], close=RUA['Close'], window=10)
# Daily returns
SPX['Return'] = SPX['Close'].pct_change()
RUA['Return'] = RUA['Close'].pct_change()
# StDev of daily returns
SPX['StDev'] = SPX['Return'].std()
RUA['StDev'] = RUA['Return'].std()

# Side column if MA10 > MA200 1 (long), else -1 (short)
SPX['Side'] = np.where(SPX['MA10'] > SPX['MA200'], 1, -1) 
RUA['Side'] = np.where(RUA['MA10'] > RUA['MA200'], 1, -1)

# drop values for first 200 days since no MA200
SPX.dropna(inplace=True)
RUA.dropna(inplace=True)

# backtest for long when Side is 1, cash when -1
# enter and exit on the Open
capital = 100000
SPX['Cash'] = capital
for i, r in SPX.iterrows():
    if r['Side'] == 1:
        capital += capital * r['Return']
        SPX['Cash'].loc[i] = capital
capital


from hmmlearn.hmm import GaussianHMM

##### HMM state 0 is bullish, 1 is bearish #####

rets = np.column_stack([SPX["Return"]])
hmm_model = GaussianHMM(n_components=2, covariance_type="full", n_iter=10000).fit(rets)
hidden_states = hmm_model.predict(rets)
SPX['HMM_state'] = hidden_states

rets = np.column_stack([RUA["Return"]])
hmm_model = GaussianHMM(n_components=2, covariance_type="full", n_iter=10000).fit(rets)
hidden_states = hmm_model.predict(rets)
RUA['HMM_state'] = hidden_states
