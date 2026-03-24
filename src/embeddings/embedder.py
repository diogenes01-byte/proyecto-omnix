import os
import pickle
from dotenv import load_dotenv
from openai import OpenAI

from src.ingestion.load_documents import load_pdfs
from src.preprocessing.text_cleaner import clean_documents
from src.preprocessing.chunking import process_documents
from src.config import EMBEDDING_MODEL

# Cargar variables de entorno
load_dotenv()

# Obtener API key desde .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDINGS_PATH = "data/embeddings/chunks_embeddings.pkl"


def generate_embeddings(batch_size: int = 32):
    """
    Pipeline completo:
    load → clean → chunk → embed (OpenAI)
    """

    # 1. Load
    docs = load_pdfs()

    # 2. Clean
    clean_docs = clean_documents(docs)

    # 3. Chunk
    chunks = process_documents(clean_docs)

    if not chunks:
        return []

    # Filtrar textos válidos
    valid_chunks = [c for c in chunks if c.get("text")]
    texts = [c["text"] for c in valid_chunks]

    if not texts:
        return valid_chunks

    embeddings = []

    # 4. Embeddings (batching manual)
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch
        )

        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)

    # Asignar embeddings a cada chunk
    for i, emb in enumerate(embeddings):
        valid_chunks[i]["embedding"] = emb

    return valid_chunks


def save_embeddings(chunks: list, path: str = EMBEDDINGS_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        pickle.dump(chunks, f)


def load_embeddings(path: str = EMBEDDINGS_PATH):
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


def build_or_load_embeddings(force_rebuild: bool = False):

    if not force_rebuild:
        chunks = load_embeddings()
        if chunks:
            print("✅ Embeddings cargados desde disco.")
            return chunks

    print("⚙️ Generando embeddings con OpenAI...")

    chunks = generate_embeddings()
    save_embeddings(chunks)

    print("💾 Embeddings guardados correctamente.")

    return chunks


if __name__ == "__main__":
    data = build_or_load_embeddings(force_rebuild=False)

    print(f"\nTotal embeddings: {len(data)}")

    if data and "embedding" in data[0]:
        print(f"Dimensión del embedding: {len(data[0]['embedding'])}")

        print("\nEjemplo:")
        print(data[0]["text"][:200])
        print(data[0]["embedding"][:10])