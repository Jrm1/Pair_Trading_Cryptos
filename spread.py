# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 21:53:47 2017

@author: Alessandro
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import datetime as dtm

import statsmodels as st

import seaborn as sns

import statsmodels.api as sm

from statsmodels.tsa.stattools import coint





def rolling_ols(data1, data2, window =30):

    a = np.array([np.nan] * len(data1))

    b = [np.nan] * len(data1)  # If betas required.

    y_ = data2.values

    x_ = sm.add_constant(data1)

    for n in range(window, len(data1)):

        y = y_[(n - window):n]

        X = x_[(n - window):n]

        # betas = Inverse(X'.X).X'.y

        betas = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

        b[n] = betas[1].tolist()  # If betas required.

    return b





def find_spread_rolling(data, name1, name2):

    

    S1 = data[name1]

    S2 = data[name2]

    

    b=rolling_ols(S1, S2, window =60)

    spread = S2 - b * S1

    spread.name = 'spread'



    # Get the 1 day moving average of the price spread

    spread_mavg1 = spread.rolling(window=1).mean()

    spread_mavg1.name = 'spread 1d mavg'



    # Get the 30 day moving average

    spread_mavg30 = spread.rolling(window=90,win_type='hamming',center=False).mean()

    spread_mavg30.name = 'spread 30d mavg'

    

    

    # Take a rolling 30 day standard deviation

    std_30 = spread.rolling(window=60).std()

    std_30.name = 'std 30d'



    # Compute the z score for each day

    zscore_30_1 = (spread_mavg1 - spread_mavg30)/std_30

    zscore_30_1.name = 'z-score'

    

    #plotting

#    plt.figure()
#
#    plt.plot(spread_mavg1.index, spread_mavg1.values)
#
#    plt.plot(spread_mavg30.index, spread_mavg30.values)
#
#    plt.legend(['1 Day Spread MAVG', '30 Day Spread MAVG'])
#
#    plt.title(name1+" "+name2)
#
#    plt.ylabel('Spread');
#
#    
#
#    
#
#    plt.figure()
#
#    zscore_30_1.plot()
#
#    plt.title(name1+" "+name2)
#
#    plt.axhline(0, color='black')
#
#    plt.axhline(1.0, color='red', linestyle='--');
#
#    plt.axhline(-1.0, color='green', linestyle='--');
#
#    
#
#    plt.figure()
#
#    plt.plot(zscore_30_1,b,'k.')
#
#    plt.title(name1+" "+name2+"scatter Zscore/beta")
#
#    plt.ylabel('beta');
#
#    plt.xlabel('Zscore');



def find_cointegrated_pairs(data):

    n = data.shape[1]

    score_matrix = np.zeros((n, n))

    pvalue_matrix = np.ones((n, n))

    keys = data.keys()

    pairs = []

    for i in range(n):

        for j in range(i+1, n):

            S1 = data[keys[i]]

            S2 = data[keys[j]]

            result = coint(S1, S2)

            score = result[0]

            pvalue = result[1]

            score_matrix[i, j] = score

            pvalue_matrix[i, j] = pvalue

            if pvalue < 0.00001:

                pairs.append((keys[i], keys[j]))

    return score_matrix, pvalue_matrix, pairs









if __name__ == "__main__":

    NC=99



    #Read the list of names 

    List = pd.read_csv('100List.csv')

    List = List.drop(['#','Market Cap', 'Price','Circulating Supply','Volume (24h)','% Change (24h)'], axis = 1)

    currencies=[]

    counter = 0

    for i in range(0,NC):

        tmp = pd.read_csv('../Top100Cryptos/'+str(List['Name'][i])+'.csv')

        if len(tmp.index) > 1000:

            

            print(str(List['Name'][i]))

            tmp = tmp.drop(['Open','High','Low','Volume','Market Cap'], axis = 1)



            tmp['Date']= pd.to_datetime(tmp['Date'], infer_datetime_format=True)



            tmp = tmp.set_index('Date')



            # sample daily

            tmp= tmp.resample('D').mean()

            currencies.append(tmp)

            counter = counter + 1

     

    NC = counter   

    for i in range(0,NC):

        currencies[i] = currencies[i].rename(columns={'Close':str(List['Name'][i])})



    # merge

    currencies = pd.concat(currencies,axis=1)







    # Drop rows with nan values (since we have different starting dates in the CSV)

    currencies = currencies.dropna(axis = 0)



    # Get column names

    column_names = currencies.keys()



    for ii in range(0,len(column_names)):

        for jj in range(ii+1,len(column_names)):

            # get the spread of two collumns

            spread = find_spread_rolling(currencies, column_names[ii],column_names[jj])


    plt.show()

    keys = currencies.keys()

    scores, pvalues, pairs = find_cointegrated_pairs(currencies)

    sns.heatmap(pvalues, xticklabels=keys.tolist(), yticklabels=keys.tolist(), cmap='RdYlGn_r', mask = (pvalues >= 0.00001))

    plt.show()

    print (pairs)

    #print (pvalues)