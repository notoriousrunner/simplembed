import json
import requests
import os

from qdrant_client import QdrantClient
from qdrant_client.http import models

QDRANT_HOST = "host.docker.internal"
QDRANT_PORT = 6333
COLLECTION_NAME = "mydocs"
N_RESULTS = 2

###functions
def embed(doc):

    if os.path.isfile(doc):
        with open(doc, 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        input_text = doc

    # Send POST request
    response = requests.post(
        "http://host.docker.internal:12434/engines/llama.cpp/v1/embeddings",
        headers={"Content-Type": "application/json"},
        json={
            "model": "ai/nomic-embed-text-v1.5",
            "input":  input_text,
            "encoding_format" : "float" 
        }
    )

    # Print the response
    print(response.status_code)

    parsed = json.loads(response.text)
    embedding_array = parsed["data"][0]["embedding"]    
    return embedding_array

def get_reply(query_emb, query, client):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_emb,
        limit=N_RESULTS  # Return N_RESULTS closest points
    )
    if results:
    
        points = results.points
        best_point = max(points, key=lambda p: p.score) if points else None
        if best_point:
            print(f"Best Document ID: {best_point.id}")
            print(f"Text:\n{best_point.payload['text']}\n")
            print(f"Similarity score: {best_point.score}\n")
            context = best_point.payload['text']

            # SmolLM2 call (assuming local Ollama)
            res = requests.post(
                "http://host.docker.internal:12434/engines/llama.cpp/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "ai/smollm2",
                    "messages": [
                        {"role": "system", "content": f"You are a helpful assistant.Answer the question based onlyon the following context: {context}, provide the citation"},
                        {"role": "user", "content": query}
                    ]
                }
            )

            data = json.loads(res.text)

            # Extract the content string
            print(data['choices'][0]['message']['content'])
        else:
            print("No points found, parsing error?")
        
    else:
        print("No docs found")
    

def process_input(input, client):
    query = embed(input)
    get_reply(query, input, client)

#initialize qdrant client
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
#do a small chat with user
while True:
    user_input = input("Enter input (type 'stop' to quit): ")
    if user_input.lower() == "stop":
        print("Stopping loop.")
        break
    process_input(user_input, client)