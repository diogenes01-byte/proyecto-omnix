from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import logging

from sentence_transformers import SentenceTransformer

from src.rag.pipeline import RAGPipeline
from src.vectorstore.store import VectorStore
from src.config import EMBEDDING_MODEL

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# App
# ---------------------------
app = FastAPI(
    title="Omnix — AI for Economic Insights",
    version="1.0.0"
)

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Schemas
# ---------------------------
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)

class Source(BaseModel):
    source: str
    chunk_id: int

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]

# ---------------------------
# Globals
# ---------------------------
rag_pipeline = None

# ---------------------------
# Startup
# ---------------------------
@app.on_event("startup")
def startup_event():
    global rag_pipeline

    try:
        logger.info("Inicializando embedder...")
        embedder = SentenceTransformer(EMBEDDING_MODEL)

        embedding_dim = embedder.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {embedding_dim}")

        logger.info("Inicializando Vector Store...")
        vector_store = VectorStore(embedding_dim=embedding_dim)

        logger.info("Inicializando RAG Pipeline...")
        rag_pipeline = RAGPipeline(vector_store=vector_store)

        logger.info("RAG Pipeline listo.")

    except Exception as e:
        logger.error(f"Error en startup: {str(e)}")
        raise e

# ---------------------------
# Endpoints
# ---------------------------
@app.get("/")
def root():
    return {"message": "RAG API activa. Endpoint: /api/v1/query"}


@app.post("/api/v1/query", response_model=QueryResponse)
def query_rag(req: QueryRequest):
    try:
        logger.info(f"Pregunta recibida: {req.question}")

        # Ejecutar pipeline
        result = rag_pipeline.query(req.question, k=5)

        answer = result["answer"]
        context_chunks = result["context"]

        if not context_chunks:
            raise HTTPException(
                status_code=404,
                detail="No se encontró contexto relevante."
            )

        sources = [
            Source(
                source=c.get("source", "unknown"),
                chunk_id=c.get("chunk_id", -1)
            )
            for c in context_chunks
        ]

        return QueryResponse(
            question=req.question,
            answer=answer,
            sources=sources
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error en query_rag: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor."
        )