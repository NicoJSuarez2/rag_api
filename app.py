from fastapi import FastAPI
import chromadb
import ollama
import os 
import logging
import asyncio
from fastapi import HTTPException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Check if mock mode is enabled first
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

if not USE_MOCK_LLM:
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama-service:11434")
    ollama_client = ollama.Client(host=ollama_host)
else:
    ollama_client = None

MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
logging.info(f"Using model: {MODEL_NAME}")
logging.info(f"Mock LLM mode: {USE_MOCK_LLM}")


app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

def run_query(q: str):
    results = collection.query(query_texts=[q], n_results=1)

    docs = results.get("documents", [])
    context = docs[0][0] if docs and docs[0] else ""

    if USE_MOCK_LLM:
        # Mock mode: return context directly
        return context
    else:
        # Real mode: use Ollama
        answer = ollama_client.generate(
            model=MODEL_NAME,
            prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
        )
        return answer["response"]


@app.post("/query")
async def query(q: str):
    try:
        logging.info(f"/query asked: {q}")
        response = await asyncio.to_thread(run_query, q)
        return {"answer": response}
        
    except Exception as e:
        logging.exception("Error en /query")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add")
def add_knowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    logging.info(f"/add received new text (id will be generated)")

    try:
        # Generate a unique ID for this document
        import uuid
        doc_id = str(uuid.uuid4())

        # Add the text to Chroma collection
        collection.add(documents=[text], ids=[doc_id])

        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@app.get("/health")
def health():
    return {"status": "ok"}
