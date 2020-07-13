!pip install nsepy

#Import the libraries
import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Taking Input
stname = input("Enter stock symbol : ")

#Fetch the data
#stock = get_history(symbol= stname, start=date(2018,7,12), end=date(2020,7,12))
#stock.reset_index()

#Was unable to fetch the data

#Load the data 
from google.colab import files
uploaded = files.upload() #upload a csv file

for fn in uploaded.keys():
  print('Uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))
  File = fn

# Store the data
stock = pd.read_csv(File)

#Set the index
stock = stock.set_index(pd.DatetimeIndex(stock['Date'].values))
StartDate = stock.iat[0,2]
EndDate = stock.iat[-1,2]

#Show the data
stock

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(stock['Close Price'],label = stname, linewidth=2)
plt.title(stname + ' Close Price History')
plt.xlabel(StartDate + ' to ' + EndDate)
plt.ylabel('Close Price INR (₹)')
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 0.5))
plt.show()

#Calculate the MACD and single line indicator
#Calculate the short term exponential moving average (EMA)
ShortEMA = stock['Close Price'].ewm(span=12, adjust=False).mean()
#Calculate the long term exponential moving average (EMA)
LongEMA = stock['Close Price'].ewm(span=26, adjust=False).mean()
#Calculate the MACD line
MACD = ShortEMA - LongEMA
#Calculate the signal line
signal = MACD.ewm(span=9, adjust=False).mean()

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(stock.index, MACD, label = stname + ' MACD', linewidth=1)
plt.plot(stock.index, signal, label = 'Signal Line', linewidth=1)
plt.title(stname + ' Indicators')
plt.xlabel(StartDate + ' to ' + EndDate)
plt.ylabel('Close Price INR (₹)')
plt.legend(loc='upper right', bbox_to_anchor=(1.175, 0.6))
plt.show()

#Create new coulmns to store all the data
stock['MACD'] = MACD
stock['Signal Line'] = signal
stock

#Create a function to signal when to buy and sell the asset/stock
def buy_sell(signal):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(0, len(signal)):
    if signal['MACD'][i] > signal['Signal Line'][i]:
      sigPriceSell.append(np.nan)
      if flag != 1:
        sigPriceBuy.append(signal['Close Price'][i])
        flag = 1
      else:
        sigPriceBuy.append(np.nan)
    elif signal['MACD'][i] < signal['Signal Line'][i]:
      sigPriceBuy.append(np.nan)
      if flag != 0:
        sigPriceSell.append(signal['Close Price'][i])
        flag = 0
      else:
        sigPriceSell.append(np.nan)
    else:
      sigPriceBuy.append(np.nan)
      sigPriceSell.append(np.nan) 

  return (sigPriceBuy, sigPriceSell)

#Store the buy and sell stock into a variable
buy_sell = buy_sell(stock)
stock['Buy_Signal_Price'] = buy_sell[0]
stock['Sell_Signal_Price'] = buy_sell[1]

#show the data
stock

#Visualize the stock
plt.figure(figsize=(13,5.2))
plt.plot(stock['Close Price'],label = stname, alpha = 0.45, linewidth=1)
plt.scatter(stock.index, stock['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
plt.scatter(stock.index, stock['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
plt.title(stname + ' Close Price History with Buy & Sell Signal')
plt.xlabel(StartDate + ' to ' + EndDate)
plt.ylabel('Close Price INR (₹)')
plt.legend(loc='upper right', bbox_to_anchor=(1.125, 0.6))
plt.show()
