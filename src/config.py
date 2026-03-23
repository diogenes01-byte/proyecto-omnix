import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Vector store
VECTORSTORE_DIR = os.path.join(DATA_DIR, "vectorstore")

# Parámetros de chunking
CHUNK_SIZE = 500 # Tamaño base para los chunks, se puede ajustar según necesidades
CHUNK_OVERLAP = 100 # Superposición entre chunks, se puede ajustar según necesidades

# Modelo de embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLM (puedes cambiar luego)
LLM_MODEL = "gpt-4o-mini"