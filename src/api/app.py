from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag.pipeline import RAGPipeline

app = FastAPI(title="RAG API - Economic Intelligence Assistant")

# Permitir CORS para que el frontend pueda hacer requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # temporalmente todo permitido
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para recibir la pregunta
class QueryRequest(BaseModel):
    question: str

# Inicializar pipeline RAG al iniciar la app
rag = RAGPipeline()


@app.get("/")
def root():
    return {"message": "RAG API está corriendo. Usa /query para hacer preguntas."}


@app.post("/query")
def query_rag(req: QueryRequest):
    # Obtener k chunks relevantes
    context_chunks = rag.retrieve(req.question, k=5)

    # Generar respuesta
    answer = rag.generate(req.question, context_chunks)

    # Preparar sources
    sources = []
    for c in context_chunks:
        source_name = c.get("source", "unknown")
        chunk_id = c.get("chunk_id", -1)
        sources.append({"source": source_name, "chunk_id": chunk_id})

    return {
        "question": req.question,
        "answer": answer,
        "sources": sources
    }