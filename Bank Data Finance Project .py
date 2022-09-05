#!/usr/bin/env python
# coding: utf-8

# In[30]:


# Install packages

import numpy as np 
import pandas as pd
import datetime as dt
import pandas_datareader as pdr
from pandas_datareader import data,wb
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Load pickle data from local drive

df = pd.read_pickle(r'D:\Python WORKBOOK\Bank Financial Capstone Project\all_banks')


# In[3]:


df.head()


# In[4]:


df.info()


# In[6]:


# Install pandas-datareader via pip 

pip install pandas-datareader


# In[36]:


# Use Yahoo Finance to retrieve daily stock price of the following banks: 

start = dt.datetime(2006, 1, 1)
end = dt.datetime(2016, 1, 1)

# Bank of America
BAC = pdr.DataReader('BAC','yahoo',start,end)

# CitiGroup
C = pdr.DataReader('C','yahoo',start,end)

# Goldman Sachs
GS = pdr.DataReader('GS','yahoo',start,end)

# JPMorgan Chase
JPM = pdr.DataReader('JPM','yahoo',start,end)

# Morgan Stanley
MS = pdr.DataReader('MS','yahoo',start,end)

# Wells Fargo
WFC = pdr.DataReader('WFC','yahoo',start,end)


# In[43]:


BAC.head()


# In[44]:


C.head()


# In[45]:


GS.head()


# In[47]:


JPM.head()


# In[48]:


MS.head()


# In[49]:


WFC.head()


# In[51]:


# Create the bank tickers in alphabetical order and call this list : tickers

tickers = ['BAC','C','GS','JPM','MS','WFC']
tickers


# In[55]:


# Use tickers as the key to create a concatenated dateframe called bank_stocks, make sure axis = 1

bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], axis=1, keys=tickers)
bank_stocks.head()


# In[58]:


# Set the column name levels 

bank_stocks.columns.names = ['Bank Ticker','Stock Info']


# In[59]:


# Check the head of the bank_stocks dataframe

bank_stocks.head()


# In[60]:


# The max Close dprice for each bank's stock throughout the time period

bank_stocks.xs('Close', axis=1, level='Stock Info').max()


# In[61]:


# Create a new empty DataFrame called returns

returns = pd.DataFrame()


# In[64]:


# Use pct_change() to create the new columns on the Close column to find the return value of each bank ticker 

for tick in tickers: 
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()


# In[65]:


returns.head()


# In[69]:


# Create the pairplot of returns dataframe

import seaborn as sns
sns.pairplot(data=returns)


# In[70]:


# Worst single day drop for each bank 

returns.idxmin()


# In[71]:


# Best single day gain for each bank

returns.idxmax()


# In[72]:


# Calculate the standard deviation of the returns for each bank stock. 

returns.std()

# Citigroup is the riskiest


# In[78]:


# Find the riskiest stock for the year of 2015 
# I tried with .ix[] to define time period but it's not working in here, so I had to use .loc[] and it works fine

returns.loc['2015-01-01':'2015-12-31'].std() 

# Bank of America and Morgan Stanley has the riskiest stock, Citigroup is also the second riskiest


# In[96]:


# Create a displot for 2015 returns of Morgan Stanley only

sns.displot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], bins = 100,kde=True)


# In[97]:


# Create a displot for 2008 returns of CitiGroup only

sns.displot(returns.loc['2008-01-01':'2008-12-31']['C Return'], bins=100, color='red', kde=True)


# In[98]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set_style('whitegrid')
import cufflinks as cf
import plotly as py
cf.go_offline()


# In[104]:


# Line plot all stocks for all banks during 2006 - 2016, using for loop 

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend()


# In[106]:


# Line plot all stocks for all banks during 2006 - 2016, using .xs()

bank_stocks.xs('Close',axis=1,level='Stock Info').plot()


# In[107]:


# Line plot all stocks for all banks during 2006 - 2016, using iplot of plotly

bank_stocks.xs('Close',axis=1,level='Stock Info').iplot()


# In[109]:


# Plot the rollling 30 days average against the Close Price for Bank of America's stock for the year 2008 

plt.figure(figsize=(12,6))
BAC['Close'].loc['2008-01-01':'2008-12-31'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].loc['2008-01-01':'2008-12-31'].plot(label='BAC CLOSE')
plt.legend()


# In[117]:


# Plot a heatmap of the correlation between the stocks Close Price

plt.figure(figsize=(12,6))
sns.heatmap(bank_stocks.xs('Close',axis=1,level='Stock Info').corr(),annot=True)


# In[124]:


# Create a clustermap to cluster the correlations of Close Price 

plt.figure(figsize=(12,6))
sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)


# In[127]:


# Create a clustermap to cluster the correlations of Close Price by using plotly

close_corr = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
close_corr.iplot(kind='heatmap',colorscale='rdylbu')


# In[131]:


# Use .iplot(kind='candle') to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016

BAC[['Open','High','Low','Close']].loc['2015-01-01':'2016-01-01'].iplot(kind='candle')


# In[133]:


# Create a Simple Moving Averages plot of Morgan Stanley for the year 2015 with .ta_plot(study='sma')

MS['Close'].loc['2015-01-01':'2015-12-31'].ta_plot(study='sma')

# Without specifying the periods, SMA only shows a single line of 14


# In[134]:


# Create a Simple Moving Averages plot of Morgan Stanley for the year 2015 with .ta_plot(study='sma')

MS['Close'].loc['2015-01-01':'2015-12-31'].ta_plot(study='sma',periods=[13,21,55],title='Simple Moving Averages')

# With periods = [13,21,55], SMA shows three lines of each value


# In[ ]:


# Create a Bollinger Band Plot for Bank of America for the year 2015 with .ta_plot() 


# In[136]:


BAC['Close'].loc['2015-01-01':'2015-12-31'].ta_plot(study='boll')


# End of project. Thank you!
