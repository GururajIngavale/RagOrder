# main.py

import time
from clean_data import update_data
from verify_db import query_strategy
from evaluate_strategy import evaluate_strategy
from order_engine import OrderEngine
import pandas as pd

engine = OrderEngine(fund=10000)

while True:
    try:
        update_data()  # update cleaned_AAPL.csv with 1m candle

        df = pd.read_csv("cleaned_AAPL.csv", skiprows=[1, 2])
        latest = df.iloc[-1]
        indicators = latest.to_dict()

        strategy_data = query_strategy(indicators)
        metadata = strategy_data["metadata"]
        strategy_text = strategy_data["strategy_text"]

        print("\n🎯 Strategy Selected:", metadata.get("title"))

        from evaluate_strategy import evaluate_strategy

        # Smart rule fallback system
        entry_rule = metadata.get("entry")
        exit_rule = metadata.get("exit")

        # If entry missing → use rule
        if not entry_rule:
            entry_rule = metadata.get("rule")

        # If still missing → NLP fallback using description
        if not entry_rule:
           print("⚠ No machine rule found. Trying NLP…")
           entry_rule = extract_rule_from_text(metadata.get("description", ""))

        # If NLP also failed → skip this round
        if not entry_rule:
            print("❌ No valid rule found (machine + NLP).")
            time.sleep(60)
            continue


        if not entry_rule:
            print("⚠ No entry rule found in metadata. Using NLP fallback...")
        
        entry_signal = evaluate_strategy(entry_rule, strategy_text, indicators)
        exit_signal = evaluate_strategy(exit_rule, strategy_text, indicators) if exit_rule else False

        price = latest["Close"]

        action = engine.process(entry_signal, exit_signal, price)
        print(f"Action: {action}, Price: {price}")

        time.sleep(60)

    except Exception as e:
        print("Loop Error:", e)
        time.sleep(60)
