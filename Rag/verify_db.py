from chromadb import PersistentClient

client = PersistentClient(path="db/strategies")
collection = client.get_collection("langchain")

def query_strategy(indicators: dict):
    text_query = ", ".join([f"{k}:{v}" for k, v in indicators.items()])

    result = collection.query(
        query_texts=[f"Market conditions: {text_query}. Find best strategy."],
        n_results=1
    )

    strategy_text = result["documents"][0][0]
    metadata = result["metadatas"][0][0]

    # Ensure new required fields exist, but do not modify existing validation logic elsewhere
    metadata.setdefault("rule", "")
    metadata.setdefault("entry", "")
    metadata.setdefault("exit", "")

    return {
        "strategy_text": strategy_text,
        "metadata": metadata
    }
