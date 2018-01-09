import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv


class DataHolder:
    def get_zscore(coins):
        #upload .csv produced by trading_signal.py
        Zscore=pd.read_csv('./data/Z_'+str(coins[0])+'-'+str(coins[1])+'.csv')
        Zscore = Zscore.dropna(axis = 0)
        Zscore=Zscore['Unnamed: 1'].tolist()

        return Zscore

    def get_beta(coins):
        beta=pd.read_csv('./data/b_'+str(coins[0])+'-'+str(coins[1])+'.csv')
        beta=beta['beta'].tolist()
    
        return beta


    def get_currencies(coins):
        currencies=[]

        for i in range(0,2):

            tmp = pd.read_csv('./data/'+str(coins[i])+'.csv')
            tmp = tmp.drop(['Open','High','Low','Volume','Market Cap'], axis = 1)
            tmp['Date']= pd.to_datetime(tmp['Date'], infer_datetime_format=True)
            tmp = tmp.set_index('Date')
            tmp= tmp.resample('D').mean()
            currencies.append(tmp)
        
        for i in range(0,2):
            currencies[i] = currencies[i].rename(columns={'Close':str(coins[i])})
    
        currencies = pd.concat(currencies,axis=1)
        currencies = currencies.dropna(axis = 0)

        keys=currencies.keys()
        name1=keys[0]
        name2=keys[1]


        return currencies, name1, name2
