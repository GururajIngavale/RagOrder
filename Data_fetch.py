import yfinance as yf


# Download BTC-USD data for last 4 years (daily candles)
btc = yf.download("GC=F",period="2y", interval="1h")


print(btc.head())


# Save data to a CSV File
btc.to_csv("Gold_History.csv")