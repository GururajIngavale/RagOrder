# 📈 SMA Crossover Visualizer & Backtester

An **interactive web-based trading strategy visualizer** and **Python backtesting script** for exploring the **SMA(20/50) crossover strategy** using historical financial data.  
Upload your OHLC CSV data, run a simple backtest, view metrics, and visualize buy/sell signals — all in your browser!

---

## 🚀 Overview

This project helps traders, quants, and learners **understand and test moving average crossovers** using two implementations:

| Component | Description |
|------------|--------------|
| 🧠 **Python Script** | Performs SMA(20/50) crossover backtest with performance metrics, PnL, drawdown, and Sharpe ratio |
| 💻 **HTML App** | Interactive browser-based visualizer using Chart.js for plotting and analysis |

---

## 🧩 Features

✅ Load & parse OHLCV CSV data (Datetime, Open, High, Low, Close, Volume)  
✅ Compute **SMA(20)** and **SMA(50)** indicators  
✅ Detect **Buy/Sell crossover signals**  
✅ Simulate long-only trades and track capital  
✅ Show key metrics:
- Total Trades
- Win Rate (%)
- Total PnL ($)
- Sharpe Ratio (approx.)
✅ Display interactive line chart with:
- SMA(20), SMA(50)
- Buy (▲) and Sell (▼) markers  
✅ Download generated trade history as `trades.csv`  
✅ Download ready-to-run `sma_crossover_backtest.py`  

---

## 🗂️ Project Structure
📦 sma-crossover-visualizer
│
├── sma_crossover_visualizer.html # Web-based visualizer (Chart.js + JS)
├── sma_crossover_backtest.py # Python backtesting script
├── Gold_History.csv # Sample OHLC data (user-provided)
└── README.md # Documentation (this file)


---

## ⚙️ Requirements

### 🐍 For Python Backtesting:
```bash
pip install pandas numpy mplfinance
🌐 For Web Visualizer:

No installation needed — just open sma_crossover_visualizer.html in your browser.

🧠 Strategy Logic

Buy Signal: SMA(20) crosses above SMA(50) → Enter long

Sell Signal: SMA(20) crosses below SMA(50) → Exit position

Each trade is executed using a fixed position size (default: $10,000)