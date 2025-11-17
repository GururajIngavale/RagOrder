import pandas as pd
import numpy as np
import talib

def update_indicators():
    df = pd.read_csv("cleaned_AAPL.csv", skiprows=[1, 2])

    # SMA
    df["sma10"] = talib.SMA(df["Close"], timeperiod=10)
    df["sma20"] = talib.SMA(df["Close"], timeperiod=20)
    df["sma50"] = talib.SMA(df["Close"], timeperiod=50)

    # EMA
    df["ema9"] = talib.EMA(df["Close"], timeperiod=9)
    df["ema21"] = talib.EMA(df["Close"], timeperiod=21)
    df["ema50"] = talib.EMA(df["Close"], timeperiod=50)

    # RSI
    df["rsi"] = talib.RSI(df["Close"], timeperiod=14)

    # MACD
    df["macd"], df["macd_signal"], df["macd_hist"] = talib.MACD(
        df["Close"], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # ATR
    df["atr"] = talib.ATR(df["High"], df["Low"], df["Close"], timeperiod=14)

    # Bollinger Bands
    df["bb_upper"], df["bb_middle"], df["bb_lower"] = talib.BBANDS(
        df["Close"], timeperiod=20, nbdevup=2, nbdevdn=2
    )
    df["bb_width"] = ((df["bb_upper"] - df["bb_lower"]) / df["Close"]) * 100

    # Volume indicators
    df["obv"] = talib.OBV(df["Close"], df["Volume"])
    df["volume_sma20"] = df["Volume"].rolling(window=20).mean()

    # VWAP
    df["vwap"] = (df["Close"] * df["Volume"]).cumsum() / df["Volume"].cumsum()

    # Support / Resistance (Pivot Points)
    df["pivot"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["resistance"] = 2 * df["pivot"] - df["Low"]
    df["support"] = 2 * df["pivot"] - df["High"]

    # Liquidity
    df["liquidity_raw"] = df["Volume"] * (df["High"] - df["Low"])
    df["liquidity_ma20"] = df["liquidity_raw"].rolling(window=20).mean()

    df.to_csv("indicators.csv", index=False)
