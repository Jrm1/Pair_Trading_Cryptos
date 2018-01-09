import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
from DataHolder import DataHolder
from Plotter import Plotter



class Backtest:

    def __init__(self):
        self.coins = ['Dash','Litecoin']
        self.position1 = [0]
        self.position2 = [0]
        self.value = [0]
        #coins=['Dash','Litecoin']
        #coins=['PIVX','Litecoin']
        #coins=['GameCredits','StellarLumens']


    def get_data(self):

        self.Zscore = DataHolder.get_zscore(self.coins)
        self.beta = DataHolder.get_beta(self.coins)
        self.currencies, self.name1, self.name2 = DataHolder.get_currencies(self.coins)


    def run_backtest(self):
            #backtest the trading strategy given by the if statements in 68 72 76-80

        for i in range(0,len(self.Zscore)):
            if self.Zscore[i]<-1.5: #sell beta coins of first currency buy one coin of the second --> the spread will narrow
                self.value.append(-self.currencies[self.name2][len(self.currencies)-len(self.beta)+i]+self.beta[i]*self.currencies[self.name1][len(self.currencies)-len(self.beta)+i])
                self.position1.append(-self.beta[i])
                self.position2.append(1)
            elif self.Zscore[i]>1.5:#buy beta coins of first currency sell one coin of the second --> the spread will narrow
                self.value.append(+self.currencies[self.name2][len(self.currencies)-len(self.beta)+i]-self.beta[i]*self.currencies[self.name1][len(self.currencies)-len(self.beta)+i])
                self.position1.append(self.beta[i])
                self.position2.append(-1)
            elif -0.5<self.Zscore[i]<0.5:#the spread is narrow-->close all positions (avoid currency 1 coins leftovers)
                self.value.append(-np.sum(self.position2)*self.currencies[self.name2][len(self.currencies)-len(self.beta)+i]-np.sum(self.position1)*self.currencies[self.name1][len(self.currencies)-len(self.beta)+i])
                self.position1.append(-np.sum(self.position1))
                self.position2.append(-np.sum(self.position2))
            else:#spread does not have a statistically significant value, wait.
                self.value.append(0)
                self.position1.append(0)
                self.position2.append(0)

        
    def plot(self):
        Plotter.plot_zscore(self.Zscore, self.name1, self.name2)
        Plotter.plot_currencies(self.currencies,self.name1, self.name2)
        Plotter.plot_pnl(self.value, self.name1, self.name2)
        Plotter.plot_logsc(self.currencies, self.beta, self.name1, self.name2)
        Plotter.plot_open_position(self.position1, self.position2, self.name1, self.name2)
        Plotter.plot_units_bought_and_sold(self.position1, self.position2, self.name1, self.name2)
        plt.show()



if __name__=="__main__":
    backtest = Backtest()
    #plotter = Plotter()
    #dataHolder = DataHolder()
    backtest.get_data()
    backtest.run_backtest()
    backtest.plot()

