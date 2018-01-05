# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 09:07:55 2018

@author: Alessandro
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import statsmodels.api as sm




if __name__ == "__main__":
    
    coins=['Dash','Litecoin']
    
    Zscore=pd.read_csv('Z_'+str(coins[0])+'-'+str(coins[1])+'.csv')
    beta=pd.read_csv('b_'+str(coins[0])+'-'+str(coins[1])+'.csv')
    
    
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
    Zscore = Zscore.dropna(axis = 0)
    
    Zscore=Zscore['Unnamed: 1'].tolist()
    beta=beta['beta'].tolist()

    keys=currencies.keys()
    name1=keys[0]
    name2=keys[1]
    
    value=[0]
    for i in range(0,len(Zscore)):
        if Zscore[i]>1:
            value.append(-currencies[name2][i]+beta[i]*currencies[name1][i])
        elif Zscore[i]<-1:
            value.append(+currencies[name2][i]-beta[i]*currencies[name1][i])
        else:
            value.append(0)
        
    
    plt.figure()

    plt.plot(value)

    plt.title(name1+" "+name2+" trades")

    plt.ylabel('instant P & L');
    
    plt.figure()

    plt.plot(np.cumsum(value))

    plt.title(name1+" "+name2+" trading")

    plt.ylabel('P & L');
    
    
    plt.figure()

    plt.semilogy(currencies[name1].index[len(currencies)-len(beta):len(currencies)],-np.min(beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])+ beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])

    plt.semilogy(currencies[name2].index[len(currencies)-len(beta):len(currencies)], -np.min(beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])+currencies[name2].values[len(currencies)-len(beta):len(currencies)])

    plt.legend(['S1 rescaled', 'S2'])

    plt.title(name1+" "+name2+" scaled prices")

    plt.ylabel('Price S2');
    
    
    
    plt.figure()

    plt.plot(Zscore)

    plt.title(name1+" "+name2+" normalised spread")

    plt.axhline(0, color='black')

    plt.axhline(1.0, color='red', linestyle='--');

    plt.axhline(-1.0, color='green', linestyle='--');
    
    plt.show()
