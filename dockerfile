FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY src/ ./src/
COPY docs/ ./docs/
COPY requirements.txt .
RUN pip install fastapi uvicorn chromadb ollama
RUN python src/embed_docs.py
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
