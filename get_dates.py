import pandas as pd

def get_unique_dates(df):
    dates = df["Date"].unique()
   # print(dates)
    return dates