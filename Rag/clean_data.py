import pandas as pd
import yfinance as yf
import time
import os

symbol = "AAPL"
csv_path = f"cleaned_{symbol}.csv"

def update_data():

    if not os.path.exists(csv_path):
        print("❌ CSV does not exist. Cannot append data.")
        return

    try:
        market_data = pd.read_csv(csv_path, skiprows=[1, 2])
    except:
        print("❌ Failed to read CSV")
        return

    market_data.rename(columns={market_data.columns[0]: 'Datetime'}, inplace=True)
    market_data['Datetime'] = pd.to_datetime(market_data['Datetime'])
    market_data.set_index('Datetime', inplace=True)

    data = yf.download(tickers=symbol, period="1d", interval="1m")

    if data is None or data.empty:
        print("⚠ No data returned from Yahoo Finance.")
        return

    latest_bar = data.iloc[[-1]]

    if latest_bar.index[-1] not in market_data.index:
        latest_bar.to_csv(csv_path, mode="a", header=False)
        print("Appended:", latest_bar.index[-1])
    else:
        print("Already up to date.")
