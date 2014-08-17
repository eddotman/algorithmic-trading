from pandas.io.data import DataReader
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
import talib
import random

print("Starting...")

#Stochastic Oscillator (Fast)
def STO(high, low, close):
    K, D = talib.STOCH(high,
                       low,
                       close,
                       fastk_period = 5,
                       slowk_period = 3,
                       slowk_matype = 0,
                       slowd_period = 3,
                       slowd_matype = 0)
    return K


start = datetime.datetime(2009, 1, 1)
end = datetime.datetime(2014, 8, 12)

#Import stock
stock = DataReader("AAPL", "yahoo", start, end)
close = stock['Close']
high = stock['High']
low = stock['Low']
STO = STO(high, low, close)

time_min = 5
time_max = 255
period_step = 5
num_starts = 100
rand_starts = random.sample(xrange(0, len(close) - time_max), num_starts)

STO_value_array = []
hold_value_array = []
STO_means = []
STO_stdev = []
hold_means = []
hold_stdev = []

print("Starting for loop...")

for time_period in range(time_min, time_max, period_step):
    for start_time in rand_starts:
        end_time = start_time + time_period
        hold_value = 1 + ( close[end_time] - close[start_time] ) / close[start_time]
        STO_value = 1
        buy_price = 0
        sell_price = 0
        own_stock = False

        for t in range(start_time, end_time):
            if STO[t] > 0 and STO[t-1] < 0: #Crosses 0 on way up:
                buy_price = close[t]
                own_stock = True
            elif STO[t] < 0 and  STO[t-1] > 0 and own_stock == True:
                sell_price = close[t]
                own_stock = False
                STO_value = STO_value*(1 + (sell_price - buy_price)/buy_price)

        #Store STO_value and hold_value in array (dynamic allocaton)
    	STO_value_array.append(STO_value)
        hold_value_array.append(hold_value)

    #Compute mean and std.dev. of the arrays
    STO_means.append(np.mean(STO_value_array))
    STO_stdev.append(np.std(STO_value_array))
    hold_means.append(np.mean(hold_value_array))
    hold_stdev.append(np.std(hold_value_array))

#Plotting
print("Plotting...")
plt.close("all")
plt.clf()
#plt.figure()
steps = np.arange(time_min, time_max, period_step)
p_STO = plt.errorbar(steps, STO_means, yerr = STO_stdev)
p_hold = plt.errorbar(steps, hold_means, yerr = hold_stdev)
plt.legend([p_STO, p_hold], ["STO", "Hold"])
plt.title("Mean return vs. length of investment")
plt.xlabel('Length of Investment')
plt.ylabel('Mean return')
plt.show()

print("Done.")

