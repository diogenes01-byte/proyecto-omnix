import os
import pickle
import time
import logging
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

from src.ingestion.load_documents import load_documents
from src.preprocessing.text_cleaner import clean_documents
from src.preprocessing.chunking import process_documents
from src.config import EMBEDDING_MODEL

load_dotenv()

logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDINGS_PATH = "data/embeddings/chunks_embeddings.pkl"


# ---------------------------
# 1. PIPELINE DATOS (SEPARADO)
# ---------------------------
def prepare_chunks() -> List[Dict[str, Any]]:
    docs = load_documents()
    clean_docs = clean_documents(docs)
    return process_documents(clean_docs)


# ---------------------------
# 2. EMBEDDINGS CON RETRY
# ---------------------------
def get_embeddings_batch(texts: List[str], retries: int = 3):
    for attempt in range(retries):
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=texts
            )
            return response.data
        except Exception as e:
            logging.warning(f"Error en embeddings (intento {attempt+1}): {e}")
            time.sleep(2)

    raise RuntimeError("Falló la generación de embeddings tras varios intentos")


def generate_embeddings(chunks: List[Dict[str, Any]], batch_size: int = 32):
    if not chunks:
        return []

    valid_chunks = [c for c in chunks if c.get("text")]

    for i in range(0, len(valid_chunks), batch_size):
        batch_chunks = valid_chunks[i:i + batch_size]
        batch_texts = [c["text"] for c in batch_chunks]

        embeddings = get_embeddings_batch(batch_texts)

        for chunk, item in zip(batch_chunks, embeddings):
            chunk["embedding"] = item.embedding

            chunk["source_metadata"] = {
                "chunk_uid": chunk.get("chunk_uid"),
                "doc_id": chunk.get("doc_id"),
                "source": chunk.get("source"),
                "chunk_id": chunk.get("chunk_id")
            }

    return valid_chunks


# ---------------------------
# 3. STORAGE
# ---------------------------
def save_embeddings(chunks: List[Dict[str, Any]], path: str = EMBEDDINGS_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        pickle.dump(chunks, f)


def load_embeddings(path: str = EMBEDDINGS_PATH):
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


# ---------------------------
# 4. PIPELINE COMPLETO
# ---------------------------
def build_or_load_embeddings(force_rebuild: bool = False):

    if not force_rebuild:
        chunks = load_embeddings()
        if chunks:
            logging.info("Embeddings cargados desde disco.")
            return chunks

    logging.info("Generando embeddings con OpenAI...")

    chunks = prepare_chunks()
    chunks = generate_embeddings(chunks)

    save_embeddings(chunks)

    logging.info("Embeddings guardados correctamente.")

    return chunks


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    data = build_or_load_embeddings(force_rebuild=False)

    print(f"\nTotal embeddings: {len(data)}")

    if data and "embedding" in data[0]:
        print(f"Dimensión del embedding: {len(data[0]['embedding'])}")

        print("\nEjemplo:")
        print(data[0]["text"][:200])
        print(data[0]["source_metadata"])