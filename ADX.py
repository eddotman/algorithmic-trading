from pandas.io.data import DataReader
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
import talib
import random

print("Starting...")

#Expects an ndarray, but got Series.
def ADX(high, low, close):
    ADX = talib.ADX(high, low, close)
    #ADXR = talib.ADXR(high, low, close)
    return ADX

def trend(high, low, close):
    PLUS_DI = talib.PLUS_DI(high, low, close)
    return PLUS_DI - MINUS_DI


start = datetime.datetime(2009, 1, 1)
end = datetime.datetime(2014, 8, 12)

#Import stock
stock = DataReader("AAPL", "yahoo", start, end)
close = stock['Close']
high= stock['High']
low = stock['Low']
ADX = ADX(high, low, close)
trend = trend(high, low ,close)

time_min = 5
time_max = 255
period_step = 5
num_starts = 100
rand_starts = random.sample(xrange(0, len(close) - time_max), num_starts)

ADX_value_array = []
hold_value_array = []
ADX_means = []
ADX_stdev = []
hold_means = []
hold_stdev = []

print("Starting for loop...")

for time_period in range(time_min, time_max, period_step):
    for start_time in rand_starts:
        end_time = start_time + time_period
        hold_value = 1 + ( close[end_time] - close[start_time] ) / close[start_time]
        ADX_value = 1
        buy_price = 0
        sell_price = 0
        own_stock = False
        ADX = ADX(high, low, close)

        for t in range(start_time, end_time):
            if ADX[t] > 20 and trend[t] > 0 and own_stock == False:
                buy_price = close[t]
                own_stock = True
            elif ADX[t] > 20 and trend[t] < 0 and own_stock == True:
                sell_price = close[t]
                own_stock = False
                ADX_value = ADX_value*(1 + (sell_price - buy_price)/buy_price)

        #Store ADX_value and hold_value in array (dynamic allocaton)
    	ADX_value_array.append(ADX_value)
        hold_value_array.append(hold_value)

    #Compute mean and std.dev. of the arrays
    ADX_means.append(np.mean(ADX_value_array))
    ADX_stdev.append(np.std(ADX_value_array))
    hold_means.append(np.mean(hold_value_array))
    hold_stdev.append(np.std(hold_value_array))

#Plotting
print("Plotting...")
plt.close("all")
plt.clf()
#plt.figure()
steps = np.arange(time_min, time_max, period_step)
p_ADX = plt.errorbar(steps, ADX_means, yerr = ADX_stdev)
p_hold = plt.errorbar(steps, hold_means, yerr = hold_stdev)
plt.legend([p_ADX, p_hold], ["ADX", "Hold"])
plt.title("Mean return vs. length of investment")
plt.xlabel('Length of Investment')
plt.ylabel('Mean return')
plt.show()

print("Done.")
