# Pair_Trading_Cryptos

-master branch updated-

The code goes through the list of 100 cryptos (available on google drive) and computes the rolling ols spread in terms of zScore. Then it plots the spread and the beta coefficient that defines the spread.

For now there is a problem when I analise more than 2 currencies. I think this might be due to the fact that currency no.3 is Bitcoin Cash that has a very short history.

If someone can fix this issue (data manipolation might be necessary) and add the statistical test for cointegration with the heat map would be good! 

Note that for convenience you can copy the code piece by piece on a Jupyter notebook and debug it there. However I think makes more sense  here to commit to a classic .py file 
