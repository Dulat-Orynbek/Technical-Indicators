import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np


class MovingAverageRSIStrategy:
    def __init__(self, capital, stock, start, end, short_period, long_period):
        self.data = None
        self.is_long = False
        self.short_period = short_period
        self.long_period = long_period
        self.capital = capital
        self.equity = [capital]
        self.stock = stock
        self.start = start
        self.end = end
    
    def download_data(self):
        stock_data = {}
        ticker =  yf.download(self.stock, self.start, self.end)
        stock_data['Price'] = ticker['Adj Close']
        self.data = pd.DataFrame(stock_data)

    def construct_signals(self):
        self.data['short MA'] = self.data['Price'].ewm(span = self.short_period, adjust = False).mean()
        self.data['long MA'] = self.data['Price'].ewm(span = self.long_period, adjust = False).mean()
        self.data['move'] = self.data['Price'] - self.data['Price'].shift(1)
        self.data['up'] = np.where(self.data['move'] > 0, self.data['move'], 0)
        self.data['down'] = np.where(self.data['move'] < 0, self.data['move'], 0)
        self.data['average gain'] = self.data['up'].rolling(14).mean()
        self.data['average loss'] = self.data['down'].rolling(14).mean()
        rs = self.data['average gain'] / self.data['average loss']
        self.data['rsi'] = 100.0 - (100.0/(1.0+rs))
        self.data = self.data.dropna()
        print(self.data)
    
    def plot_signals(self):
        plt.figure(figsize=(12,6))
        plt.plot(self.data['Price'], label = 'Price')
        plt.plot(self.data['short MA'], label = 'Short MA', color = 'red')
        plt.plot(self.data['long MA'], label = 'Long MA', color = 'blue')
        plt.title('MovingAVGcrossoverStrategy with RSI')
        plt.xlabel('Date')
        plt.ylabel('Stock Prices')
        plt.show()

    def simulate(self):
        price_when_buy =  0
        for index, row in self.data.iterrows():
            #close
            if row['short MA']<row['long MA'] and self.is_long:
                self.equity.append(self.capital*row['Price']/price_when_buy)
                self.is_long = False
                
            elif row['short MA']>row['long MA'] and not self.is_long and row['rsi'] < 30:   
                price_when_buy = row['Price']
                self.is_long = True

    def plot_equity(self):
        
        plt.figure(figsize=(12,6))
        plt.title("Equity Curve")
        plt.plot(self.equity, label='Stock Prices', color='green')
        plt.xlabel('Date')
        plt.ylabel('Capital($)')
        plt.show()

    def show_stats(self):
        profit_percentage = (float(self.equity[-1]) - float(self.equity[0])) / (float(self.equity[0])) * 100
        print("Profit of the trading strategy: %.2f%%" % profit_percentage)
        print("Actual capital: %.2f" % self.equity[-1])
        returns = (self.data['Price'] - self.data['Price'].shift(1))/self.data['Price'].shift(1)
        ratio = returns.mean()/returns.std()*np.sqrt(252)
        print('Sharpe Ratio: %.2f' %ratio)


if __name__ == '__main__':
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime(2020, 1, 1)

    model = MovingAverageRSIStrategy(100, 'AAPL', start, end, 30, 100           )
    model.download_data()
    model.construct_signals()
    model.plot_signals()
    model.simulate()
    model.plot_equity()
    model.show_stats()

    