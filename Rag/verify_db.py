from chromadb import PersistentClient 
from indicators import latest_data
import time

client  = PersistentClient(path = "db/strategies")
collection =  client.get_collection("langchain")

time.sleep(5)

current_market = latest_data()

results = collection.query(
    query_texts = [f" {current_market}  \n Find me the best stratergy for the given conditions above  "],
    n_results =3 
)

for i in range (len(results['ids'][0])) : 
    print ("Strategy :", results ['documents'][0][i][:100])