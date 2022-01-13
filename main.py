import re
import math
import pandas as pd
import numpy as np
import get_dates
import run_simulation as rs
import run_simulation2 as rs2

desired_width=320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns',10)




months_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]
loc = "/home/nonu/Downloads/2020/"

yearly_profit = 0

results = []

for m in months_list:
    path = loc + "Monthly Segregated/" + m + "/" + "BANKNIFTY.csv"
    df = pd.read_csv(path,header=None)
    df.columns = ['Ticker', 'Date', 'Time', 'Open',"High","Low","Close","Vol","X"]
    df = df.drop(['Vol', 'X'], axis=1)
    monthly_trading_dates = get_dates.get_unique_dates(df)
    d = dict(tuple(df.groupby('Date')))
    x=0
    for date in monthly_trading_dates:
        profit = rs.backtest(d[date])
        entry = [date]
        entry.extend(profit)
        results.append(entry)
        x+=profit[4]

    yearly_profit+=x


df = pd.DataFrame(results, columns =['Date','Buy','S1','Sell','S2','Profit'])
df['ProfitTillDate'] = df['Profit'].cumsum()
print(df)
df.to_excel("./Rwsults/trailingSL_ORB.xlsx")




