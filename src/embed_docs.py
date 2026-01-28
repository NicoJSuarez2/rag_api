import chromadb
import os

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

# Clear existing documents (if any)
existing_ids = collection.get()["ids"]
if existing_ids:
    collection.delete(ids=existing_ids)

# Get the path to the docs directory (parent of src)
docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

# Embed all files in docs/ folder
for filename in os.listdir(docs_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, "r") as f:
            text = f.read()
            collection.add(documents=[text], ids=[filename])

print("Re-embedded all documents in docs/ folder")
