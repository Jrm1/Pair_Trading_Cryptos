## Pair_Trading_Cryptos

The spread.py code goes through the list of 100 cryptos and computes via rolling ols the normalised spread. Then it plots the spread and the beta coefficient that defines the spread. Finally it provides cointegration test for all pairs in the form of heatmap; small p values can be highlighted for convenience.

Note that for convenience you can copy the code piece by piece on a Jupyter notebook and debug it there. However I think makes more sense  here to commit to a classic .py file 

-Monero not fixed yet-

# Pairs folder

The folder Pairs contains trading_signal.py and backtest.py and all the .csv files containing coins data.
 
trading_signal.py requires you to specify the pair you want to analyse (coins=[]), then it gives you some flexibility on the window types to use for the moving average and the least square rescaling (window_s, window_ols). The program outputs two .csv files with the normalised spread and the ols coefficients. 

backtest.py makes use of the output of trading_signal.py. It runs over the normalised spread and applies a trading strategy (for now very simple defined in figure strategy.jpg). The program records the instantaneous cash position and plots some informative plots (example in figure example_backtest.jpg).