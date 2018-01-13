import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
from DataHolder import DataHolder
from Plotter import Plotter

class Trading:


    def __init__(self):
        self.coins = ['Dash','Litecoin'] #choose your coins
        self.window_ols = 60 #choose the width of the window for the estimation of beta (the wider the smoother)
        self.window_ma = 60 #choose the lookback period for the moving average to build the Zscore (more robust for slower ma)

    def get_data(self):
        self.currencies, self.name1, self.name2 = DataHolder.get_currencies(self.coins)

    def rolling_ols(self):
        self.N=len(self.currencies[self.name1])
        self.beta = [np.nan] * self.N
        y_ = self.currencies[self.name2]
        x_ = sm.add_constant(self.currencies[self.name1])
        # we are using an rectangular window here
        for n in range(self.window_ols, self.N):
            Y = y_[(n - self.window_ols):n]
            X = x_[(n - self.window_ols):n]
            b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
            self.beta[n] = b[1].tolist()

    def find_Zscore(self):
        spread = self.currencies[self.name2] - self.beta * self.currencies[self.name1]
        spread.name = 'spread'
        # Get the 1 day moving average of the price spread
        spread_mavg1 = spread.rolling(window=1).mean()
        spread_mavg1.name = 'spread 1d mavg'
        # Get the longer moving average
        spread_mavg = spread.rolling(window=self.window_ma,win_type='hamming',center=False).mean()
        spread_mavg.name = 'spread mavg'
        # Take a rolling standard deviation
        spread_std = spread.rolling(window=self.window_ma).std()
        spread_std.name = 'standard deviation'
        # Compute the z score for each day
        self.Zscore = (spread_mavg1 - spread_mavg)/spread_std

    def printer(self):
        self.Zscore.to_csv('./data/Z_'+str(self.name1)+'-'+str(self.name2)+'.csv')
        self.beta = pd.DataFrame(self.beta, columns=["beta"])
        self.beta.to_csv('./data/b_'+str(self.name1)+'-'+str(self.name2)+'.csv', index=False)

    def plot(self):
        Plotter.plot_zscore(self.Zscore, self.name1, self.name2)
        Plotter.plot_currencies(self.currencies,self.name1, self.name2)
        plt.show()


if __name__ == "__main__":

    trading=Trading()
    trading.get_data()
    trading.rolling_ols()
    trading.find_Zscore()
    trading.printer()
    trading.plot()