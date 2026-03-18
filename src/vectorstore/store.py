import faiss
import numpy as np
from src.embeddings.embedder import generate_embeddings


class VectorStore:

    def __init__(self):
        self.index = None
        self.texts = []
        self.metadata = []

    def build_index(self):
        data = generate_embeddings()

        embeddings = np.array([d["embedding"] for d in data]).astype("float32")

        self.texts = [d["text"] for d in data]
        self.metadata = [{"source": d["source"], "chunk_id": d["chunk_id"]} for d in data]

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        print(f"Index creado con {self.index.ntotal} vectores")

    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            results.append({
                "text": self.texts[i],
                "metadata": self.metadata[i]
            })

        return results


from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

if __name__ == "__main__":
    vs = VectorStore()
    vs.build_index()

    model = SentenceTransformer(EMBEDDING_MODEL)

    query = "What does the ECB say about inflation?"
    query_embedding = model.encode([query]).astype("float32")

    results = vs.search(query_embedding, k=3)

    print("\nResultados:\n")
    for r in results:
        print(r["metadata"])
        print(r["text"][:300])
        print("-" * 50)