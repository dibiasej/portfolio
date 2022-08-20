import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from pandas_datareader import get_data_yahoo as pdr 
import datetime as dt 
import os

def portfolio_return(start, end, **tickers):

	all_ticker_data = pd.DataFrame()

	if end == 'today':

		for ticker, quantity in tickers.items():

			df = pdr(ticker, dt.datetime(start, 1, 1), dt.datetime.now())
			df[ticker] = df['Adj Close'] * quantity
			df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], 1, inplace = True)
			all_ticker_data = pd.concat([all_ticker_data, df], axis = 1)

	else:
		for ticker, quantity in tickers.items():
			df = pdr(ticker, dt.datetime(start, 1, 1), dt.datetime(end, 1, 1))
			df[ticker] = df['Adj Close'] * quantity
			df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], 1, inplace = True)
			all_ticker_data = pd.concat([all_ticker_data, df], axis = 1)

	portfolio = pd.DataFrame(all_ticker_data)

	#all_ticker_data.to_csv('portfolio.csv', index = True)

	#portfolio = pd.read_csv('portfolio.csv', parse_dates = True)

	#portfolio.index = portfolio['Date']

	#del portfolio['Date']

	columns = portfolio.columns

	portfolio['Total Assets'] = 0


	for column in columns:
		portfolio['Total Assets'] += portfolio[column]

	portfolio['Log Returns'] = np.log(portfolio['Total Assets']/portfolio['Total Assets'].shift(1))

	return(portfolio['Log Returns'].cumsum().apply(np.exp).plot(figsize=(12,8)))

