import chromadb
import os

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

# Get the path to the docs directory (parent of src)
docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "k8s.txt")

with open(docs_path, "r") as f:
    text = f.read()

collection.add(documents=[text], ids=["k8s"])

print("Embedding stored in Chroma")
