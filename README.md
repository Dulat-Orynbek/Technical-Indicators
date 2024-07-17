#Moving Average & Relative strength crossover strategy

This repository contains code snippets of creating and implementing Moving Average & Relative strength crossover strategy
      The principle components on which strategy works are indicating moments of crossover of slow-moving-average-line(long_period) by fast-moving-average-line(short_period) and crossing relative strength lines            (<0.3 rsi means stock is oversold -> the price will increase in future)
Sharpe ratio and simulations were used to measure profitability and raliability of strategy
Sharpe ratio ~0.3 and unstable profits showed that this model is too simple to rely on
The code is written in Python. Libraries : pandas, yfinance, numpy, matplotlib, datetime
Guided by Holczer Balazs
