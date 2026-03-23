from sentence_transformers import SentenceTransformer

from src.vectorstore.store import VectorStore
from src.config import EMBEDDING_MODEL


class Retriever:

    def __init__(self):
        print("Inicializando Retriever...")

        # Cargar modelo de embeddings
        print("Cargando modelo de embeddings...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

        # Determinar dimensión del embedding
        embedding_dim = len(self.embedder.encode(["test"])[0])

        # Inicializar VectorStore
        self.vs = VectorStore(embedding_dim)

        # 🔴 Cargar datos desde el .pkl
        self.vs.load_from_pickle("data/embeddings/chunks_embeddings.pkl")

    def retrieve(self, query: str, k: int = 5):
        """
        Recupera los k chunks más relevantes para una query
        """

        # Embedding de la query
        query_embedding = self.embedder.encode([query]).astype("float32")

        # Búsqueda en FAISS
        results = self.vs.search(query_embedding, k=k)

        return results


# -------------------------
# Test rápido en consola
# -------------------------
if __name__ == "__main__":
    retriever = Retriever()

    query = "What is inflation?"
    results = retriever.retrieve(query, k=3)

    print("\nResultados:\n")

    for i, r in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(r["text"][:300])
        print("Metadata:", r.get("metadata", {}))
        print("Score:", r.get("score"))
        print()