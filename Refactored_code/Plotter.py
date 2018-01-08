


class Plotter:

    def plot_zscore(Zscore, name1, name2):

        plt.figure()
        plt.plot(Zscore)
        plt.title(name1+" "+name2+" normalised spread")
        plt.axhline(0, color='black')
        plt.axhline(1.0, color='red', linestyle='--');
        plt.axhline(-1.0, color='green', linestyle='--');
        plt.show()
    

    def plot_currencies(currencies,name1,name2):

        plt.figure()
        plt.semilogy(currencies[str(name1)])
        plt.semilogy(currencies[str(name2)])
        plt.legend([str(name1), str(name2)])
        plt.title(name1+" "+name2)
        plt.ylabel('$ (log-scale)');


    def plot_pnl(value, name1, name2):

        plt.figure()
        plt.plot(np.cumsum(value))
        plt.title(name1+" "+name2+" P&L")
        plt.ylabel('P & L');


    def plot_logsc(currencies,beta, name1, name2):

        plt.figure()
        plt.plot(currencies[name1].index[len(currencies)-len(beta):len(currencies)],-np.min(beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])+ beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])
        plt.plot(currencies[name2].index[len(currencies)-len(beta):len(currencies)], -np.min(beta*currencies[name1].values[len(currencies)-len(beta):len(currencies)])+currencies[name2].values[len(currencies)-len(beta):len(currencies)])
        plt.legend([str(name1)+' rescaled', str(name2)])
        plt.title(name1+" "+name2+" scaled prices")
        plt.ylabel('$ (log-scale)');


    def plot_open_position(position1, name1, name2):

        plt.figure()
        plt.plot(np.cumsum(position1))
        plt.plot(np.cumsum(position2))
        plt.legend([str(name1), str(name2)])
        plt.title(name1+" "+name2+" portfolio positions")
        plt.ylabel('coins-holding (# of coins)');


    def units_bought_and_sold(position1, name1, name2):
    
        plt.figure()
        plt.plot(position1)
        plt.plot(position2)
        plt.legend([str(name1), str(name2)])
        plt.title(name1+" "+name2+" trades")
        plt.ylabel('units bought and sold');
