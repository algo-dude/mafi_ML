import pandas as pd
# xls to df
df = pd.read_excel('spxcalls20160331.xlsx')

SP_value = 2059.74
SP_moneyness = [SP_value*.8, SP_value*1.2]
# filter df to be within SP_moneyness
df= df[(df['Strike']>SP_moneyness[0]) & (df['Strike']<SP_moneyness[1])]

mlist = df.Maturity.unique()
mlist = list(mlist)
mlist.sort()
# Remove every other maturity so that 8 remain.
# could add one week to a maturity with datetime.timedelta(days=7)
mlist = mlist[::2]
mlist
# Filter df to only include mlist.
df = df[df['Maturity'].isin(mlist)]

# interest rate is .01, dividend rate is .02, r-d = -.01
r = .01
d = .02

r = r - d

S = SP_value
sigma = .2

import numpy as np
from scipy.stats import norm

df['IV'] = 0
df['TTM'] = 0

# TTM is days to maturity
df['TTM'] = (df['Maturity'] - df['Date']).dt.days
# sort df by TTM
df.sort_values(by=['TTM', 'Strike'], inplace=True)

#
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad
# mpl.rcParams['font.family'] = 'serif'


def dN(x):
    ''' Probability density function of standard normal random variable x. '''
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def N(d):
    ''' Cumulative density function of standard normal random variable x. '''
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


def d1f(St, K, T, r, sigma):
    ''' Black-Scholes-Merton d1 function.
        Parameters see e.g. BSM_call_value function. '''
    d1 = (math.log(St / K) + (r + 0.5 * sigma ** 2)
          * (T )) / (sigma * math.sqrt(T ))
    return d1

# Valuation Functions
#

def BSM_vega(St, K, T, r, sigma):
    ''' Black-Scholes-Merton VEGA of European call option.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    vega : float
        European call option VEGA
    '''
    d1 = d1f(St, K, T, r, sigma)
    vega = St * dN(d1) * math.sqrt(T )
    return vega
    
def BSM_call_value(St, K, T, r, sigma):
    ''' Calculates Black-Scholes-Merton European call option value.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    call_value : float
        European call present value at t
    '''
    d1 = d1f(St, K, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T )
    call_value = St * N(d1) - math.exp(-r * (T )) * K * N(d2)
    return call_value


def implied_volatility_call(C, S, K, T, r, tol=0.00001,
                            max_iterations=50):
    '''
    :param C: Observed call price
    :param S: Asset price
    :param K: Strike Price
    :param T: Time to Maturity
    :param r: riskfree rate
    :param tol: error tolerance in result
    :param max_iterations: max iterations to update vol
    :return: implied volatility in percent
    '''
    ### assigning initial volatility estimate for input in Newton_rap procedure
    sigma = 0.1

    for i in range(max_iterations):

        ### calculate difference between blackscholes price and market price with
        ### iteratively updated volality estimate
        diff = BSM_call_value(S, K, T, r, sigma) - C

        ###break if difference is less than specified tolerance level
        if abs(diff) < tol:
            print(f'found on {i}th iteration')
            print(f'difference is equal to {diff}')
            break

        ### use newton rapshon to update the estimate
        sigma = sigma - diff / BSM_vega(S, K, T, r, sigma)

    return sigma

# Call implied volatility function on each row to compare market Call price to estimated BSM price
# When they equal, we have determined the implied volatility
# iterate throudh df and apply implied volatility function to each row
for i, row in df.iterrows():
    print ('row', i)
    df.loc[i, 'IV'] = implied_volatility_call(row['Call'], S, row['Strike'], row['TTM'], r)

# df['IV'] = df.apply(lambda row: implied_volatility_call(row['Call'], S, row['Strike'], row['TTM'], r), axis=1)

# X = df['Strike'], Y = df['TTM'], Z = df['IV']
plot_df = df[['Strike', 'TTM', 'IV']]

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import seaborn as sns
# Make the plot
fig = plt.figure()
ax = plt.axes(projection='3d')
surf = ax.plot_trisurf(plot_df['Strike'], plot_df['TTM'], plot_df['IV'], cmap=plt.cm.viridis, linewidth=0.2)
fig.colorbar(surf, shrink=0.5, aspect=5)
# ax.set_title('SPX Vol Surface')
ax.set_xlabel('Strike')
ax.set_ylabel('TTM')
ax.set_zlabel('IV')
# rotate the image here
ax.view_init(elev=10, azim=-80)
plt.title('SPX Vol Surface', fontsize=20)
# make image larger
# for some reason, run this cell twice to make the image larger?
plt.rcParams['figure.figsize'] = (20, 20)
plt.show()
 