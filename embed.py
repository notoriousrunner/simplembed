import json
import requests
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models

QDRANT_HOST = "host.docker.internal"
QDRANT_PORT = 6333
COLLECTION_NAME = "mydocs"

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

#   Qdrant client Initialization
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Create a collection if it doesn't exist
#if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
if not client.collection_exists(collection_name=COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
    )
# Documents
documents = {
    1: open("doc1.txt", encoding="utf-8").read(),
    2: open("doc2.txt", encoding="utf-8").read()
}

# For each document, get the embedding and upload in Qdrant
for doc_id, text in documents.items():
    print(f"uploading{doc_id}")
    emb = embed(text)
    print(f"embedding done, uploading {doc_id} on the DB")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[models.PointStruct(id=doc_id, vector=emb, payload={"text": text})]
    )
