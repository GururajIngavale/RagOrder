import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

with open("strategies.json" , "r" , encoding="utf-8") as f : 
    strategies = json.load(f)

texts = []
metadatas = []

for s in strategies :
    text = f" {s['title']}. {s['description']}. {s['rules']}. {s['indicators_used']}. {s['signal_logic']}. {s['entry_rules']}. {s['exit_rules']}. {s['best_timeframe']}. {s['objective']}. "
    texts.append(text)

    metadatas.append ( { "id" : s["id"] ,  "tags": ", ".join(s.get("tags", [])) , "source" : s["source"] , "performance" : s["performance"] , "market" : s["market"] , "image" : s.get("image ", None) })
    
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_texts(
    texts = texts , 
    metadatas = metadatas ,
    embedding = embedding_model ,
    persist_directory = "db/strategies"
)

db.persist()
print("Saved to Chroma DB")

