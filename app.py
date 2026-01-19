from fastapi import FastAPI
import chromadb
import ollama
import os
import logging
import uuid
import time

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# -------------------------------------------------
# Config
# -------------------------------------------------
MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama:latest")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://evolutionapi_ollama:11434")

logging.info(f"Using model: {MODEL_NAME}")
logging.info(f"Ollama host: {OLLAMA_HOST}")

# -------------------------------------------------
# App
# -------------------------------------------------
app = FastAPI()

# -------------------------------------------------
# Chroma
# -------------------------------------------------
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

# -------------------------------------------------
# Ollama helpers
# -------------------------------------------------
def get_ollama_client():
    if not hasattr(app.state, "ollama"):
        app.state.ollama = ollama.Client(host=OLLAMA_HOST)
    return app.state.ollama


@app.on_event("startup")
def startup_event():
    logging.info("Waiting for Ollama...")

    for i in range(10):
        try:
            client = get_ollama_client()
            models = client.list()
            logging.info(f"Ollama ready. Models: {models}")
            return
        except Exception as e:
            logging.warning(f"Ollama not ready yet ({i+1}/10): {e}")
            time.sleep(2)

    raise RuntimeError("Ollama is not available after retries")

# -------------------------------------------------
# Endpoints
# -------------------------------------------------
@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""

    client = get_ollama_client()

    answer = client.generate(
        model=MODEL_NAME,
        prompt=f"""Context:
{context}

Question: {q}

Answer clearly and concisely:""",
    )

    logging.info(f"/query asked: {q}")

    return {"answer": answer["response"]}


@app.post("/add")
def add_knowledge(text: str):
    doc_id = str(uuid.uuid4())
    collection.add(documents=[text], ids=[doc_id])

    logging.info(f"/add received new text (id={doc_id})")

    return {
        "status": "success",
        "id": doc_id
    }


@app.get("/health")
def health():
    return {"status": "ok"}
