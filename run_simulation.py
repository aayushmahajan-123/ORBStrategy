import re
import math
import pandas as pd
import numpy as np
import get_dates

desired_width=320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns',10)





def backtest(df):
    trigger_buy = 0
    trigger_sell = 0
    stoploss_buy = 0
    stoploss_sell = 0

    df_first_15 = df.head(15)
    highs = df_first_15["High"]
    lows = df_first_15["Low"]
    trigger_buy = highs.max()
    trigger_sell = lows.min()
    stoploss_buy = trigger_buy - 0.05*trigger_buy
    stoploss_sell = trigger_sell + 0.05*trigger_sell

    #print([trigger_buy,trigger_sell,stoploss_buy,stoploss_sell])

    df = df.tail(-15)
    #calculate stoploss based on closing price
    df["StoplossBuy"]=df["Low"]-df["Low"]*0.005
    df["StoplossSell"] = df["High"] + df["High"] * 0.005


    Buy_Price = -1
    Sell_Price = -1
    Stop1 = -1
    Stop2 = -1



    profit= 0
    InTrade = False
    StopHit = False
    TradeType = ""

    for idx,row in df.iterrows():
        L = row["Low"]
        H = row["High"]

        if StopHit:
            break
        if row["Time"]=="15:15":
            if InTrade and TradeType=="Buy":
                profit = -trigger_buy + row["Close"]
                Stop1 = row["Close"]
            if InTrade and TradeType == "Sell":
                profit = -row["Close"] + trigger_sell
                Stop2 = row["Close"]
            break

        if InTrade:
            if TradeType == "Buy":
                if L <= stoploss_buy:
                    profit = -trigger_buy + min(stoploss_buy,H)
                    Stop1 = min(stoploss_buy,H)
                    StopHit = True
                stoploss_buy = row["StoplossBuy"]

            if TradeType == "Sell":
                if H >= stoploss_sell:
                    profit = -max(stoploss_sell,L)+trigger_sell
                    Stop2 = max(stoploss_sell,L)
                    StopHit = True
                stoploss_sell = row["StoplossSell"]

        if not InTrade:
            if H >= trigger_buy:
                trigger_buy = max(trigger_buy,L)
                InTrade = True
                stoploss_buy = trigger_buy - 0.005*trigger_buy
                TradeType = "Buy"
                Buy_Price = trigger_buy
            elif L<=trigger_sell:
                trigger_sell = min(trigger_sell,H)
                InTrade = True
                stoploss_sell = trigger_sell + 0.005*trigger_sell
                TradeType = "Sell"
                Sell_Price = trigger_sell

    return [Buy_Price,Stop1,Sell_Price,Stop2,profit]









