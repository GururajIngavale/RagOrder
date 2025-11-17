from evaluate_strategy import evaluate_strategy

# sample indicators
ind = {"sma20": 10, "sma50": 9, "rsi": 55}

rule = "sma20 > sma50 and rsi < 70"

print("Rule:", rule)
print("Evaluation:", evaluate_strategy(rule, ind))
