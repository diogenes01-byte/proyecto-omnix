from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import logging

from src.rag.pipeline import RAGPipeline
from src.vectorstore.store import VectorStore

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
    chunk_uid: int | None = None
    source: str
    chunk_id: int | None = None

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
        logger.info("Inicializando Vector Store...")

        vector_store = VectorStore()
        vector_store.load_from_pickle()

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
        if rag_pipeline is None:
            raise HTTPException(status_code=500, detail="Pipeline no inicializado")

        logger.info(f"Pregunta recibida: {req.question}")

        result = rag_pipeline.query(req.question, k=5)

        answer = result["answer"]
        sources = result.get("sources", [])

        if not sources:
            return QueryResponse(
                question=req.question,
                answer="No se encontró contexto relevante en la base de datos.",
                sources=[]
            )

        # 🔥 ya no reconstruimos nada, solo normalizamos salida
        formatted_sources = [
            Source(
                chunk_uid=s.get("chunk_uid"),
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

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Error en query_rag: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor."
        )