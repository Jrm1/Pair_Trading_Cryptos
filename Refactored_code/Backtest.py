import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
__import__(DataHolder)
__import__(Plotter)


class Backtest:

    def __init__(self):
        self.coins = ['Dash','Litecoin']
        self.positions1 = [0]
        self.positions1 = [0]
        self.value = [0]
        #coins=['Dash','Litecoin']
        #coins=['PIVX','Litecoin']
        #coins=['GameCredits','StellarLumens']


    def get_data(DataHolder):
                
        Zscore = DataHolder.get_zscore(self.coins)
        beta = DataHolder.get_beta(self.coins)
        currencies, name1, name2 = DataHolder.get_currencies(self.coins)

        return Zscore, beta, currencies, name1, name2

    def run_backtest():
            #backtest the trading strategy given by the if statements in 68 72 76-80
        value=[0]
        position1=[0]
        position2=[0]
        for i in range(0,len(Zscore)):
            if Zscore[i]<-1.5: #sell beta coins of first currency buy one coin of the second --> the spread will narrow
                value.append(-currencies[name2][len(currencies)-len(beta)+i]+beta[i]*currencies[name1][len(currencies)-len(beta)+i])
                position1.append(-beta[i])
                position2.append(1)
            elif Zscore[i]>1.5:#buy beta coins of first currency sell one coin of the second --> the spread will narrow
                value.append(+currencies[name2][len(currencies)-len(beta)+i]-beta[i]*currencies[name1][len(currencies)-len(beta)+i])
                position1.append(beta[i])
                position2.append(-1)
            elif -0.5<Zscore[i]<0.5:#the spread is narrow-->close all positions (avoid currency 1 coins leftovers)
                value.append(-np.sum(position2)*currencies[name2][len(currencies)-len(beta)+i]-np.sum(position1)*currencies[name1][len(currencies)-len(beta)+i])
                position1.append(-np.sum(position1))
                position2.append(-np.sum(position2))
            else:#spread does not have a statistically significant value, wait.
                value.append(0)
                position1.append(0)
                position2.append(0)
        
        
    def plot(Plotter):
        Plotter.plot_zscore(Zscore, name1,name2)
        Plotter.plot_currencies(currencies,name1,name2)
        Plotter.plot_pnl(value, name1, name2)
        Plotter.plot_logsc(currencies,beta, name1, name2)
        Plotter.plot_open_position(position1, name1, name2)
        Plotter.units_bought_and_sold(position1, name1, name2)
        

