import pandas as pd
import yfinance as yf
import time 

symbol = "AAPL"
csv_path = f"cleaned_{symbol}.csv"

def update_data() :

    # Load the existing CSV
    market_data = pd.read_csv(csv_path , skiprows= [1,2])
    market_data.rename(columns={market_data.columns[0]: 'Datetime'}, inplace=True)
    market_data['Datetime'] = pd.to_datetime(market_data['Datetime'])
    market_data.set_index('Datetime', inplace=True)

    # Get latest data
    data = yf.download(tickers=symbol, period="1d", interval="5m")
    latest_bar = data.iloc[[-1]]

    # Append only if new
    if latest_bar.index[-1] not in market_data.index:
        latest_bar.to_csv(csv_path, mode='a', header=False)
        print("Appended:", latest_bar.index[-1])
    else:
        print("Already up to date.")

while True : 
    update_data()
    time.sleep(300)
