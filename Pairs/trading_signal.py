# -*- coding: utf-8 -*-
"""
Created on 04/01/2018

@author: Alessandro
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import statsmodels.api as sm

import csv




def rolling_ols(data1, data2, window ):

    b = [np.nan] * len(data1)

    y_ = data2.values

    x_ = sm.add_constant(data1)
    
    # we are using an rectangular window here

    for n in range(window, len(data1)):

        Y = y_[(n - window):n]

        X = x_[(n - window):n]

        beta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)

        b[n] = beta[1].tolist()

    return b





def find_spread_rolling(data,window_ols,window_s):

    keys=data.keys()
    name1=keys[0]
    name2=keys[1]

    S1 = data[name1]

    S2 = data[name2]

    b=rolling_ols(S1, S2, window_ols )

    spread = S2 - b * S1

    spread.name = 'spread'



    # Get the 1 day moving average of the price spread

    spread_mavg1 = spread.rolling(window=1).mean()

    spread_mavg1.name = 'spread 1d mavg'



    # Get the longer moving average

    spread_mavg = spread.rolling(window=window_s,win_type='hamming',center=False).mean()

    spread_mavg.name = 'spread mavg'

    

    # Take a rolling standard deviation

    spread_std = spread.rolling(window=window_s).std()

    spread_std.name = 'standard deviation'



    # Compute the z score for each day

    Zscore = (spread_mavg1 - spread_mavg)/spread_std

    Zscore.name = 'Z-score'

    

    #plotting
    
    plt.figure()

    plt.plot(spread_mavg1.index,b,'k-')

    plt.title(name1+" "+name2+" beta")

    plt.ylabel('beta');
    

    plt.figure()

    plt.plot(S1.index, b*S1.values)

    plt.plot(S2.index, S2.values)

    plt.legend(['S1 rescaled', 'S2'])

    plt.title(name1+" "+name2+" scaled prices")

    plt.ylabel('Price S2');
    
    
    
    plt.figure()

    plt.plot(spread_mavg1.index, spread_mavg1.values)

    plt.plot(spread_mavg.index, spread_mavg.values)

    plt.legend(['1 Day Spread ', ' Spread MAVG'])

    plt.title(name1+" "+name2+" spread")

    plt.ylabel('Spread');

    

    

    plt.figure()

    Zscore.plot()

    plt.title(name1+" "+name2+" normalised spread")

    plt.axhline(0, color='black')

    plt.axhline(1.0, color='red', linestyle='--');

    plt.axhline(-1.0, color='green', linestyle='--');
    
    return Zscore, b



if __name__ == "__main__":


    window_ols=120
    window_s=90
    coins=['Dash','Litecoin']
    #coins=['PIVX','Vertcoin']


    currencies=[]

    for i in range(0,2):

        tmp = pd.read_csv(str(coins[i])+'.csv')

        tmp = tmp.drop(['Open','High','Low','Volume','Market Cap'], axis = 1)

        tmp['Date']= pd.to_datetime(tmp['Date'], infer_datetime_format=True)

        tmp = tmp.set_index('Date')

        # sample daily

        tmp= tmp.resample('D').mean()

        currencies.append(tmp)
        
    for i in range(0,2):
        currencies[i] = currencies[i].rename(columns={'Close':str(coins[i])})
    
    currencies = pd.concat(currencies,axis=1)
    currencies = currencies.dropna(axis = 0)

    Zscore, beta = find_spread_rolling(currencies,window_ols,window_s)
    plt.show()
    
    Zscore.to_csv('Z_'+str(coins[0])+'-'+str(coins[1])+'.csv')
    beta = pd.DataFrame(beta, columns=["beta"])
    beta.to_csv('b_'+str(coins[0])+'-'+str(coins[1])+'.csv', index=False)
