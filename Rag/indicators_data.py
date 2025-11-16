import pandas as pd
import numpy as np
import talib


def update_indicators ()  :
    df = pd.read_csv("cleaned_AAPL.csv", skiprows=[1,2])

    # --- SMA INDICATORS
    df['SMA_10'] = talib.SMA(df['Close'], timeperiod=10)
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
        
    # --- EMA INDICATORS ---
    df["EMA_9"] = talib.EMA(df["Close"], timeperiod=9)
    df["EMA_21"] = talib.EMA(df["Close"], timeperiod=21)
    df["EMA_50"] = talib.EMA(df["Close"], timeperiod=50)

        # --- MOMENTUM INDICATORS ---
    df["RSI_14"] = talib.RSI(df["Close"], timeperiod=14)
    df["MACD"], df["MACD_signal"], df["MACD_hist"] = talib.MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)

    # --- VOLATILITY INDICATORS ---
    df["ATR_14"] = talib.ATR(df["High"], df["Low"], df["Close"], timeperiod=14)
    df["BB_upper"], df["BB_middle"], df["BB_lower"] = talib.BBANDS(df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2)
    df["BB_width"] = ((df["BB_upper"] - df["BB_lower"]) / df["Close"]) * 100  

    # --- VOLUME INDICATORS ---
    df["OBV"] = talib.OBV(df["Close"], df["Volume"])
    df["Vol_Avg20"] = df["Volume"].rolling(window=20).mean()

    # --- VWAP (Bias Indicator) ---
    df["VWAP"] = (df["Close"] * df["Volume"]).cumsum() / df["Volume"].cumsum()

    # --- SUPPORT / RESISTANCE (Pivot Points) ---
    df["Pivot"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["R1"] = 2 * df["Pivot"] - df["Low"]
    df["S1"] = 2 * df["Pivot"] - df["High"]

    # --- PRICE CHANGE ---
    df["Price_Change_Pct"] = df["Close"].pct_change() * 100

    # --- Liquidity indicator ---
    df["Liquidity_Raw"] = df["Volume"] * ( df["High"] - df["Low"])
    df["Liquidity_20MA"] = df["Liquidity_Raw"].rolling(window=20).mean()

    df.to_csv("indicators.csv") 
    