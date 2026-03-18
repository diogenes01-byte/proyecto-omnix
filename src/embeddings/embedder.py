from sentence_transformers import SentenceTransformer
from src.preprocessing.chunking import process_documents
from src.config import EMBEDDING_MODEL


def generate_embeddings():
    model = SentenceTransformer(EMBEDDING_MODEL)

    chunks = process_documents()
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    for i, emb in enumerate(embeddings):
        chunks[i]["embedding"] = emb

    return chunks


if __name__ == "__main__":
    data = generate_embeddings()

    print(f"\nTotal embeddings generados: {len(data)}")
    print(f"Dimensión del embedding: {len(data[0]['embedding'])}")

    # Preview
    print("\nEjemplo:")
    print(data[0]["text"][:200])
    print(data[0]["embedding"][:10])  # primeros valores