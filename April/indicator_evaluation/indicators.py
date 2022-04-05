import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data
import warnings
warnings.filterwarnings("ignore")

def author():
    return "these are not the droids you are looking for"


def getprices(symbol, start_date, end_date):
    prices = get_data(symbol, pd.date_range(start_date, end_date))
    if 'SPY' not in symbol:
        prices.drop('SPY', axis=1, inplace=True)

    prices = prices.fillna(method='ffill')
    prices = prices.fillna(method='bfill')
    prices_normed = prices / prices.iloc[0]
    return prices_normed


# Indicator 1 - Simple Moving Average
def getsma(prices, moving_window):
    sma = prices.rolling(window=moving_window).mean()
    sma_by_price = sma / prices
    sma_50_days = prices.rolling(window=50).mean()
    return sma, sma_by_price, sma_50_days


# Indicator 2 - Bollinger Bands Percentage
def getBBP(prices, moving_window):
    rolling_mean = prices.rolling(window=moving_window).mean()
    rolling_std = prices.rolling(window=moving_window).std()
    upperband = rolling_mean + (2 * rolling_std)
    lowerband = rolling_mean - (2 * rolling_std)
    BBP = (prices - lowerband) / (upperband - lowerband)
    return upperband, lowerband, BBP


# Indicator 3 - Momentum
def getMomentum(prices, moving_window):
    momentum = prices / prices.shift(moving_window) - 1
    return momentum


# Indicator 4 - Volatility
def getVolatility(prices, moving_window):
    daily_returns = prices.copy()
    daily_returns[1:] = (prices[1:] / prices[:-1].values) - 1
    daily_returns = daily_returns[1:]
    volatility = daily_returns.rolling(window=moving_window).std()
    return volatility

# Indicator 5  - MACD
def getMACD(prices):
    ema_short = prices.ewm(span=12, adjust=False).mean()
    ema_long = prices.ewm(span=26, adjust=False).mean()
    MACD = ema_long - ema_short
    signal = MACD.ewm(span=9, adjust=False).mean()
    return MACD, signal

def test_code_indicators(symbol = "JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):

    moving_window = 14
    prices = getprices([symbol], sd, ed)

    # Indicator 1 - plotting SMA
    sma, sma_by_price, sma_50_days = getsma(prices, moving_window)
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

    # Indicator 2 - plotting Bollinger Bands
    upperband, lowerband, BBP = getBBP(prices, moving_window)
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

    # Indicator 3 - plotting Momentum
    momentum = getMomentum(prices, moving_window)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Momentum")
    ax.plot(prices, "goldenrod", label='Normalized Price')
    ax.plot(momentum, "blue", label="Momentum")
    ax.legend()
    fig.savefig('Indicator3_Momentum.png')
    plt.close()

    # Indicator 4 - plotting Volatility
    volatility = getVolatility(prices, moving_window)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="Volatility")
    ax.plot(prices, "goldenrod", label='Normalized Price')
    ax.plot(volatility, label="Volatility")
    ax.legend()
    fig.savefig('Indicator4_Volatility.png')
    plt.close()

    # Indicator 5 - plotting MACD
    MACD, signal = getMACD(prices)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set(xlabel='Time', ylabel="Price", title="MACD")
    ax.plot(MACD, "gray", label='MACD')
    ax.plot(signal, "coral", label="MACD Signal")
    ax.legend()
    fig.savefig('Indicator5_MACD.png')
    plt.close()