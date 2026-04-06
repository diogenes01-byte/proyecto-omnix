from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import logging

from src.rag.pipeline import RAGPipeline
from src.vectorstore.store import VectorStore
from src.config import EMBEDDING_DIM

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
    allow_origins=["*"],
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
    chunk_uid: str | None = None
    source: str = "unknown"
    chunk_id: int | None = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]

# ---------------------------
# Startup
# ---------------------------
@app.on_event("startup")
def startup_event():
    try:
        logger.info("Inicializando Vector Store...")

        vector_store = VectorStore(embedding_dim=EMBEDDING_DIM)
        vector_store.load_from_pickle()

        logger.info("Inicializando RAG Pipeline...")

        app.state.rag_pipeline = RAGPipeline(vector_store=vector_store)

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
        rag_pipeline = getattr(app.state, "rag_pipeline", None)

        if rag_pipeline is None:
            raise HTTPException(status_code=500, detail="Pipeline no inicializado")

        logger.info(f"Pregunta recibida: {req.question}")

        result = rag_pipeline.query(req.question, k=5)

        answer = result.get("answer", "")
        sources = result.get("sources", [])

        logger.info("Respuesta generada correctamente.")

        if not sources:
            return QueryResponse(
                question=req.question,
                answer="No se encontró contexto relevante en la base de datos.",
                sources=[]
            )

        # ---------------------------
        # FIX: normalización de tipos
        # ---------------------------
        formatted_sources = [
            Source(
                chunk_uid=str(s.get("chunk_uid")) if s.get("chunk_uid") is not None else None,
                source=s.get("source", "unknown"),
                chunk_id=s.get("chunk_id")
            )
            for s in sources
        ]

        return QueryResponse(
            question=req.question,
            answer=answer,
            sources=formatted_sources
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error en query_rag: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor."
        )