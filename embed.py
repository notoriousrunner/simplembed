import json
import numpy as np
import requests
import os


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

# Function cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_reply(query_emb, query):
    sim1 = cosine_similarity(doc1_emb, query_emb)
    sim2 = cosine_similarity(doc2_emb, query_emb)

    if sim1 > sim2:
        chosen = "doc1.txt"
    else:
        chosen = "doc2.txt"
    print (f"with a similarity of {sim1} against {sim2} system decided for {chosen}")
    with open(chosen, encoding="utf8") as f:
        context = f.read()

    # Prompt for SmolLM2
    prompt = f"Query: {query} Context: {context}"

    # SmolLM2 call (assuming local Ollama)
    res = requests.post(
        "http://host.docker.internal:12434/engines/llama.cpp/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        #    json={
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

def process_input(input):
    query = embed(input)
    get_reply(query, input)

#start embedding documents
print("embedding bio")
doc1_emb = embed("doc1.txt")
print("embedding tax")
doc2_emb = embed("doc2.txt")

#do a small chat with user
while True:
    user_input = input("Enter input (type 'stop' to quit): ")
    if user_input.lower() == "stop":
        print("Stopping loop.")
        break
    process_input(user_input)