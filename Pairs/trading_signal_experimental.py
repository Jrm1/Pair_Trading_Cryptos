# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:22:47 2018

@author: Alessandro
"""

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


#this function computes the rolling linear relation between the two coins

def rolling_ols(data1, data2, data3, window ):

    b1 = [np.nan] * len(data1)
    b2 = [np.nan] * len(data1)

    y_ = data3.values

    tmp = np.array([data1, data2])
    x_ =sm.add_constant(tmp.T)


    # we are using an rectangular window here
    for n in range(window, len(data1)):

        Y = y_[(n - window):n]

        X = x_[(n - window):n]

        model = sm.OLS(Y,X).fit()

        b1[n] = model.params[1]
        b2[n] = model.params[2]

    return b1, b2



#this function computes the normalised spread

def find_spread_rolling(data,window_ols,window_s):

    keys=data.keys()
    name1=keys[0]
    name2=keys[1]
    name3=keys[2]

    S1 = data[name1]

    S2 = data[name2]

    S3 = data[name3]

    b1, b2=rolling_ols(S1, S2, S3, window_ols )

    spread = S3 - b1 * S1 - b2 * S2

    spread.name = 'spread'
    
    beta=np.array([b1,b2])

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

    plt.plot(spread_mavg1.index,b1,'k-')
    
    plt.plot(spread_mavg1.index,b2,'k--')
    
    plt.legend([name1,name2])


    plt.title(name1+" "+name2+" "+name3+" beta")

    plt.ylabel('beta');
    

    plt.figure()

    plt.plot(S1.index, b1*S1.values)

    plt.plot(S2.index, b2*S2.values)

    plt.plot(S3.index, S3.values)

    plt.legend([name1+'rescaled', name2+'rescaled', name3])

    plt.title(name1+" "+name2+" "+name3+" scaled prices")

    plt.ylabel('Price S3');
    
    
    
    plt.figure()

    plt.plot(spread_mavg1.index, spread_mavg1.values)

    plt.plot(spread_mavg.index, spread_mavg.values)

    plt.legend(['1 Day Spread ', ' Spread MAVG'])

    plt.title(name1+" "+name2+" "+name3+" spread")

    plt.ylabel('Spread');

    

    

    plt.figure()

    Zscore.plot()

    plt.title(name1+" "+name2+" "+name3+" normalised spread")

    plt.axhline(0, color='black')

    plt.axhline(1.0, color='red', linestyle='--');

    plt.axhline(-1.0, color='green', linestyle='--');
    
    return Zscore, beta



if __name__ == "__main__":


    window_ols=30
    window_s=60
    coins=['Dash','Litecoin','Ethereum']
    #coins=['Ethereum','Litecoin']
    #coins=['GameCredits','StellarLumens','Litecoin']



    currencies=[]

    for i in range(0,3):

        tmp = pd.read_csv(str(coins[i])+'.csv')

        tmp = tmp.drop(['Open','High','Low','Volume','Market Cap'], axis = 1)

        tmp['Date']= pd.to_datetime(tmp['Date'], infer_datetime_format=True)

        tmp = tmp.set_index('Date')

        # sample daily

        tmp= tmp.resample('D').mean()

        currencies.append(tmp)
        
    for i in range(0,3):
        currencies[i] = currencies[i].rename(columns={'Close':str(coins[i])})

    currencies = pd.concat(currencies,axis=1)
    currencies = currencies.dropna(axis = 0)
    currencies = currencies.drop(currencies.index[[range(600)]],axis = 0)


    Zscore, beta= find_spread_rolling(currencies,window_ols,window_s)
    plt.show()
    
    Zscore.to_csv('Z_'+str(coins[0])+'-'+str(coins[1])+'-'+str(coins[2])+'.csv')
    beta = pd.DataFrame(beta)
    beta.to_csv('b_'+str(coins[0])+'-'+str(coins[1])+'-'+str(coins[2])+'.csv', index=False)
