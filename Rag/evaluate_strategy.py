# evaluate_strategy.py

import ast
import operator as op
import math

# -----------------------------------------------------------
# 1) NLP FALLBACK RULE EXTRACTOR (LIGHTWEIGHT BUT EFFECTIVE)
# -----------------------------------------------------------

def nlp_extract_rule(text: str) -> str:
    """
    Convert natural English strategy text → machine-readable backup rule.
    Triggered only when JSON rule is missing or invalid.
    """

    text = text.lower()
    rules = []

    # --- Trend ---
    if any(t in text for t in ["uptrend", "bullish", "higher highs"]):
        rules.append("sma20 > sma50")

    if any(t in text for t in ["downtrend", "bearish", "lower highs"]):
        rules.append("sma20 < sma50")

    # --- RSI ---
    if "oversold" in text:
        rules.append("rsi < 30")
    if "overbought" in text:
        rules.append("rsi > 70")

    # --- Breakout / Breakdown ---
    if "breakout" in text:
        rules.append("close > vwap")
    if "breakdown" in text:
        rules.append("close < vwap")

    # --- Volume ---
    if any(t in text for t in ["high volume", "volume spike"]):
        rules.append("volume > volume_sma20")

    if not rules:
        return ""   # fallback still fails → invalid strategy

    return " and ".join(rules)



# -----------------------------------------------------------
# 2) SAFE AST RULE ENGINE (EXECUTES MACHINE RULES)
# -----------------------------------------------------------

allowed_ops = {
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,

    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,

    ast.Gt: op.gt,
    ast.Lt: op.lt,
    ast.GtE: op.ge,
    ast.LtE: op.le,
    ast.Eq: op.eq,
    ast.NotEq: op.ne
}

allowed_functions = {
    "abs": abs,
    "sqrt": math.sqrt,
    "max": max,
    "min": min
}


def safe_eval_node(node, vars):
    if isinstance(node, ast.BinOp):
        return allowed_ops[type(node.op)](
            safe_eval_node(node.left, vars),
            safe_eval_node(node.right, vars)
        )

    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(safe_eval_node(v, vars) for v in node.values)
        else:
            return any(safe_eval_node(v, vars) for v in node.values)

    if isinstance(node, ast.Compare):
        return allowed_ops[type(node.ops[0])](
            safe_eval_node(node.left, vars),
            safe_eval_node(node.comparators[0], vars)
        )

    if isinstance(node, ast.Call):
        func = allowed_functions.get(node.func.id)
        args = [safe_eval_node(a, vars) for a in node.args]
        return func(*args)

    if isinstance(node, ast.Name):
        return vars.get(node.id, 0)

    if isinstance(node, ast.Constant):
        return node.value

    raise ValueError("Unsupported expression")



# -----------------------------------------------------------
# 3) MASTER EVALUATOR (PRIMARY + NLP FALLBACK)
# -----------------------------------------------------------

def evaluate_strategy(rule: str, strategy_text: str, indicators: dict) -> bool:
    """
    Main strategy evaluator:
    1) Try strict machine rule (entry/exit from JSON)
    2) If fails -> use NLP fallback to auto-fix rule
    """

    # --- STEP 1: Direct machine-readable rule (preferred) ---
    if rule and rule.strip() != "":
        try:
            expression = ast.parse(rule, mode="eval")
            return safe_eval_node(expression.body, indicators)
        except:
            print("⚠ Machine rule failed. Trying NLP fallback…")

    # --- STEP 2: NLP fallback (auto repair) ---
    fallback_rule = nlp_extract_rule(strategy_text)

    if fallback_rule == "":
        print("❌ No valid rule found (machine + NLP).\n")
        return False

    print("🔁 Using NLP fallback rule:", fallback_rule)

    try:
        expression = ast.parse(fallback_rule, mode="eval")
        return safe_eval_node(expression.body, indicators)
    except Exception as e:
        print("❌ NLP fallback failed:", e)
        return False
