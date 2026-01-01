# ⚡Rag Order — RAG-Powered Algo Trading Engine⚡

Real-Time Market Analysis • AI Strategy Retrieval • Automated Trade Execution

![Status](https://img.shields.io/badge/STATUS-ACTIVE-brightgreen?style=for-the-badge)
![Tech](https://img.shields.io/badge/TECH-RAG-blue?style=for-the-badge)
![Automation](https://img.shields.io/badge/TRADING-AUTOMATION-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/MADE_WITH-PYTHON-yellow?style=for-the-badge)

---

## 🚀 Overview

**StrategyPulse** is a modern algorithmic trading engine designed to leverage:

* **Retrieval-Augmented Generation (RAG)** for intelligent strategy selection
* **Real-time market data** for continuous analysis
* **Technical indicators** using TA-LIB
* **Natural language → executable rule conversion**
* **Automated BUY/SELL execution** with P&L tracking

StrategyPulse monitors the market in real time, retrieves the most relevant trading strategy from ChromaDB, evaluates rule conditions, and executes trades automatically.

---

## 🧠 How It Works

1. **Live Market Feed** – `clean_data.py` updates real-time 1-minute OHLCV data.
2. **Indicator Engine** – `indicators_data.py` computes SMA, EMA, RSI, MACD, ATR, VWAP, OBV, Bollinger Bands, and more.
3. **RAG Strategy Retrieval** – `verify_db.py` fetches best-matched strategies from the vector DB.
4. **NL Strategy → Machine Rule** – `evaluate_strategy.py` converts natural-language rules into executable expressions.
5. **Trading Execution** – `order_engine.py` executes BUY/SELL/HOLD decisions and logs trades.
6. **Master Loop** – `main.py` orchestrates the entire pipeline.

---

## 🏗️ Architecture Diagram

```
clean_data.py           →  Fetch live 1m data
↓
indicators_data.py      →  Compute technical indicators
↓
verify_db.py            →  Retrieve best strategy via RAG
↓
evaluate_strategy.py    →  Convert & evaluate rule conditions
↓
order_engine.py         →  Execute trades (BUY / SELL / HOLD)
↓
main.py                 →  Master loop controller
```

---

## 📁 Project Structure

```
Rag/
├── clean_data.py
├── indicators_data.py
├── verify_db.py
├── evaluate_strategy.py
├── order_engine.py
├── create_embeddings.py
├── strategies.json
├── indicators.json
├── main.py
│
├── cleaned_AAPL.csv
├── indicators.csv
├── pnl_log.csv
│
└── db/strategies/     # Vector DB for RAG
```

---

## 🛠️ Tech Stack

### Core Components

* 🐍 **Python**
* 🧠 **ChromaDB** (Vector database)
* ✨ **HuggingFace MiniLM embeddings**
* 📉 **TA-LIB** (Indicators)
* 💹 **YFinance** (Live market data)
* 📦 **Pandas / NumPy**
* 📁 **OpenPyXL** (Excel output)
* 🔍 **Regex + AST** (Rule interpretation)

---

## ⚙️ Installation

### 1) Clone the Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/Rag
```

### 2) Create a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 3) Install Requirements

```bash
pip install -r requirements.txt
```

### 📌 Build the Strategy Vector DB

```bash
python create_embeddings.py
```

**Expected output:**

```
Saved to Chroma DB
```

---

## ▶️ Run the Complete System

```bash
python main.py
```

**Sample output:**

```
📊 Indicators Loaded
🎯 Strategy Selected: Multi-Timeframe Trend
📝 Extracted Rule: sma20 > sma50 and rsi > 55
⚡ Action: BUY
💼 Trade Executed Successfully
```

---

## 📊 Generated Files

| File               | Description                      |
| ------------------ | -------------------------------- |
| `cleaned_AAPL.csv` | Live market feed data            |
| `indicators.csv`   | Technical indicator calculations |
| `pnl_log.csv`      | P&L + trade logs                 |
| `db/strategies/`   | Chroma vector database           |

---

## 🔮 Future Roadmap

* Multi-symbol support
* Real brokerage integration (Zerodha / IBKR / Binance)
* Backtesting engine
* Live dashboard for P&L and strategy monitoring
* LLM-powered automated strategy generation

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome.
Feel free to open an issue or submit a PR.

---

## ⭐ Support

If you find this project useful, please consider leaving a **GitHub Star ⭐**!
