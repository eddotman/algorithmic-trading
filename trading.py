from pandas.io.data import DataReader
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
import talib
import random

class Trader:

  def __init__(self):
    pass #Do nothing for now

  #MACD: Moving Average Convergence/Divergence
  def MACD(self, close):
    macd_shrt_in = 12
    macd_long_in = 26
    macd_signal_in = 9
    ta_macd =  talib.MACD(np.array(close), macd_shrt_in, macd_long_in, macd_signal_in)[2]

    return ta_macd

  def ADX(high, low, close):
    ADX = talib.ADX(high, low, close)
    #ADXR = talib.ADXR(high, low, close)
    return ADX

  def trend(high, low, close):
    PLUS_DI = talib.PLUS_DI(high, low, close)
    return PLUS_DI - MINUS_DI

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


if __name__ == '__main__':

  print("Starting...")

  start = datetime.datetime(2009, 1, 1)
  end = datetime.datetime(2014, 8, 12)

  #Import stock
  stock = DataReader("AAPL", "yahoo", start, end)
  close = stock['Adj Close']

  time_min = 5
  time_max = 255
  period_step = 5
  num_starts = 100
  rand_starts = random.sample(xrange(0, len(close) - time_max), num_starts)

  MACD_value_array = []
  hold_value_array = []
  MACD_means = []
  MACD_stdev = []
  hold_means = []
  hold_stdev = []

  trader = Trader()

  print("Starting for loop...")

  for time_period in range(time_min, time_max, period_step):
    for start_time in rand_starts:
      end_time = start_time + time_period
      hold_value = 1 + ( close[end_time] - close[start_time] ) / close[start_time]
      MACD_value = 1
      buy_price = 0
      sell_price = 0
      own_stock = False
      macd = trader.MACD(close)

      for t in range(start_time, end_time):
        if macd[t] > 0 and macd[t-1] < 0: #Crosses 0 on way up:
          buy_price = close[t]
          own_stock = True
        elif macd[t] < 0 and  macd[t-1] > 0 and own_stock == True:
          sell_price = close[t]
          own_stock = False
          MACD_value = MACD_value*(1 + (sell_price - buy_price)/buy_price)

      #Store MACD_value and hold_value in array (dynamic allocaton)
      MACD_value_array.append(MACD_value)
      hold_value_array.append(hold_value)

      #Compute mean and std.dev. of the arrays
      MACD_means.append(np.mean(MACD_value_array))
      MACD_stdev.append(np.std(MACD_value_array))
      hold_means.append(np.mean(hold_value_array))
      hold_stdev.append(np.std(hold_value_array))

  #Plotting
  print("Plotting...")
  plt.close("all")
  plt.clf()
  #plt.figure()
  steps = np.arange(time_min, time_max, float(period_step)/float(num_starts))
  #p_macd = plt.plot(steps, MACD_means)
  p_macd = plt.errorbar(steps, MACD_means, yerr = MACD_stdev)
  p_hold = plt.errorbar(steps, hold_means, yerr = hold_stdev)
  plt.legend([p_macd, p_hold], ["MACD", "Hold"])
  plt.title("Mean return vs. length of investment")
  plt.xlabel('Length of Investment')
  plt.ylabel('Mean return')
  plt.show()

  print("Done.")


  #Possible extensions of this code
  #1) Record how much time MACD is holding money for.
  #   Probably ~40%, which means it it missing out on some gains
  #2) Record 'trendiness', i..e use ADX method and try to corrolate trend and profit.
  #3) Repeat for other indicators
  #4)
