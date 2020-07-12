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
#data = get_history(symbol= stname, start=date(2018,7,12), end=date(2020,7,12))
#data.reset_index()

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

#Show the Data
stock

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(stock['Close Price'],label = stname)
plt.title(stname + ' Close Price History')
plt.xlabel(StartDate + ' to ' + EndDate)
plt.ylabel('Close Price INR (₹)')
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 0.5))
plt.show()

# Creating a simple moving averag for 30 days
SMA30 = pd.DataFrame()
SMA30['Close Price'] = stock['Close Price'].rolling(window=30).mean()
SMA30

# Creating a simple moving averag for 100 days
SMA100 = pd.DataFrame()
SMA100['Close Price'] = stock['Close Price'].rolling(window=100).mean()
SMA100

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(stock['Close Price'],label = stname)
plt.plot(SMA30['Close Price'],label = 'SMA30')
plt.plot(SMA100['Close Price'],label = 'SMA100')
plt.title(stname + ' Close Price History')
plt.xlabel(StartDate + ' to ' + EndDate)
plt.ylabel('Close Price INR (₹)')
plt.legend(loc='upper right', bbox_to_anchor=(1.125, 0.6))
plt.show()

#Create a new data frame to store all the data
data= pd.DataFrame()
data['stock'] = stock['Close Price']
data['SMA30'] = SMA30['Close Price']
data['SMA100'] = SMA100['Close Price']
data

#Create a function to signal when to buy and sell the asset/stock
def buy_sell(data):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(len(data)):
    if data['SMA30'][i] > data['SMA100'][i]:
      if flag != 1:
        sigPriceBuy.append(data['stock'][i])
        sigPriceSell.append(np.nan)
        flag = 1
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    elif data['SMA30'][i] < data['SMA100'][i]:
      if flag != 0:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(data['stock'][i])
        flag = 0
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    else:
      sigPriceBuy.append(np.nan)
      sigPriceSell.append(np.nan) 

  return (sigPriceBuy, sigPriceSell)

#Store the buy and sell data into a variable
buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

#show the data
data

#Visualize the data
plt.figure(figsize=(13,5.2))
plt.plot(stock['Close Price'],label = stname, alpha = 0.45)
plt.plot(data['SMA30'],label = 'SMA30', alpha = 0.45)
plt.plot(data['SMA100'],label = 'SMA100', alpha = 0.45)
plt.scatter(data.index, data['Buy_Signal_Price'], label = 'Buy', marker = '^', color = 'green')
plt.scatter(data.index, data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color = 'red')
plt.title(stname + ' Close Price History with Buy & Sell Signal')
plt.xlabel(StartDate + ' to ' + EndDate)
plt.ylabel('Close Price INR (₹)')
plt.legend(loc='upper right', bbox_to_anchor=(1.125, 0.6))
plt.show()
