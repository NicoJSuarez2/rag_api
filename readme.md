# RAG API - Retrieval Augmented Generation

API REST para consultas RAG usando ChromaDB y Ollama.

## 🚀 Características

- ✅ **RAG (Retrieval Augmented Generation)**: Combina búsqueda semántica con LLM
- ✅ **ChromaDB**: Base de datos vectorial para embeddings
- ✅ **Ollama**: LLM local para generación de respuestas
- ✅ **FastAPI**: Framework web moderno y rápido
- ✅ **Modo Mock**: Para testing sin necesidad de Ollama

## 📂 Estructura del Proyecto

```
rag_api_/
├── src/                      # Código fuente
│   ├── main.py              # API principal
│   ├── embed.py             # Embeddings de k8s.txt
│   └── embed_docs.py        # Embeddings de todos los docs
├── docs/                     # Documentos para RAG
├── test/                     # Tests
├── k8s/                      # Manifiestos de Kubernetes
├── db/                       # Base de datos ChromaDB
└── requirements.txt
```

## 🔧 Instalación

```bash
# Clonar repositorio
git clone https://github.com/NicoJSuarez2/rag_api.git
cd rag_api

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Embeddings iniciales
python src/embed_docs.py
```

## 🏃 Ejecución

### Desarrollo Local (con Ollama)
```bash
# Iniciar Ollama primero
ollama serve

# Ejecutar API
python main.py
# o
uvicorn src.main:app --reload
```

### Modo Mock (sin Ollama - para testing)
```bash
USE_MOCK_LLM=1 uvicorn src.main:app --reload
```

## 🧪 Testing

El modo mock permite ejecutar tests **sin necesidad de Ollama**, ideal para CI/CD:

```bash
# Modo mock: retorna el contexto directamente
USE_MOCK_LLM=1 python main.py

# Ejecutar tests
python test/semantic_test.py
```

### CI/CD (GitHub Actions)

El workflow `.github/workflows/ci.yaml` ejecuta automáticamente en modo mock:

```yaml
- name: Start API in mock mode
  run: |
    USE_MOCK_LLM=1 uvicorn src.main:app --host 0.0.0.0 --port 8000 &
```

✅ **No requiere Ollama en el runner de GitHub**  
✅ **Tests determinísticos** (misma entrada = misma salida)  
✅ **Más rápido** que usar LLM real

## 🐳 Docker

```bash
# Build
docker build -t rag-api .

# Run con Ollama externo
docker run -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  rag-api

# Run en modo mock
docker run -p 8000:8000 \
  -e USE_MOCK_LLM=1 \
  rag-api
```

## ☸️ Kubernetes

```bash
kubectl apply -f k8s/
```

## 📝 API Endpoints

### POST /query
Consulta al RAG

```bash
curl -X POST "http://localhost:8000/query?q=What is Kubernetes?"
```

### POST /add
Agregar contenido a la base de conocimientos

```bash
curl -X POST "http://localhost:8000/add?text=New knowledge here"
```

### GET /health
Health check

```bash
curl http://localhost:8000/health
```

## 🔐 Variables de Entorno

- `USE_MOCK_LLM`: `1` para modo mock, `0` para producción (default)
- `OLLAMA_HOST`: URL del servidor Ollama (default: `http://ollama-service:11434`)
- `MODEL_NAME`: Modelo de Ollama a usar (default: `tinyllama`)

## 📄 Licencia

MIT
