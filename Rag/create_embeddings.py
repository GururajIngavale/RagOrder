import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

with open("strategies.json", "r", encoding="utf-8") as f:
    strategies = json.load(f)

texts = []
metadatas = []

for s in strategies:

    indicators_used = s.get("indicators_used", [])
    if isinstance(indicators_used, list):
        indicators_used = ", ".join(indicators_used)

    tags = s.get("tags", [])
    if isinstance(tags, list):
        tags = ", ".join(tags)

    text = (
        f"{s.get('title', '')}. "
        f"{s.get('description', '')}. "
        f"Rule: {s.get('rule', '')}. "
        f"Entry: {s.get('entry', '')}. "
        f"Exit: {s.get('exit', '')}. "
        f"Indicators: {indicators_used}. "
        f"Market: {s.get('market', '')}. "
        f"Timeframe: {s.get('timeframe', '')}."
    )

    texts.append(text)

    meta = {
        "id": str(s.get("id", "")),
        "title": s.get("title", ""),
        "rule": s.get("rule", ""),
        "entry": s.get("entry", ""),
        "exit": s.get("exit", ""),
        "indicators_used": indicators_used,
        "market": s.get("market", ""),
        "timeframe": s.get("timeframe", ""),
        "tags": tags
    }

    metadatas.append(meta)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_texts(
    texts=texts,
    metadatas=metadatas,
    embedding=embedding_model,
    persist_directory="db/strategies"
)

db.persist()
print("✅ Saved strategies into Chroma DB successfully!")
