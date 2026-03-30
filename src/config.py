import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Vector store
VECTORSTORE_DIR = os.path.join(DATA_DIR, "vectorstore")

# Embeddings
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings", "chunks_embeddings.pkl")

# Parámetros de chunking
CHUNK_SIZE = 450 # Tamaño base para los chunks, se puede ajustar según necesidades
CHUNK_OVERLAP = 90 # Superposición entre chunks, se puede ajustar según necesidades

# Modelo de embeddings
EMBEDDING_MODEL = "text-embedding-3-small"

# LLM (puedes cambiar luego)
LLM_MODEL = "gpt-4o-mini"

# Dimensión de embeddings
EMBEDDING_DIM = 1536