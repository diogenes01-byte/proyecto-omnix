import faiss
import numpy as np
import pickle
from typing import List, Dict, Any, Optional

from src.config import EMBEDDINGS_FILE, EMBEDDING_DIM


class VectorStore:
    def __init__(self, embedding_dim: int = EMBEDDING_DIM):
        self.index = faiss.IndexFlatIP(embedding_dim)

        self.texts: List[str] = []
        self.metadata: List[Dict[str, Any]] = []

    # -------------------------
    # Normalization
    # -------------------------
    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        vectors = np.array(vectors, dtype="float32")

        if len(vectors.shape) == 1:
            vectors = vectors.reshape(1, -1)

        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-10)

    # -------------------------
    # Add documents
    # -------------------------
    def add_documents(
        self,
        embeddings: np.ndarray,
        texts: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None
    ):
        embeddings = self._normalize(embeddings)

        self.index.add(embeddings)
        self.texts.extend(texts)

        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in texts])

    # -------------------------
    # Load from pickle
    # -------------------------
    def load_from_pickle(self, path: str = EMBEDDINGS_FILE):
        with open(path, "rb") as f:
            chunks = pickle.load(f)

        if not chunks:
            raise ValueError("El archivo pickle está vacío")

        embeddings = np.array([c["embedding"] for c in chunks]).astype("float32")
        texts = [c["text"] for c in chunks]

        # Metadata completa para RAG tracing
        metadata = [
            {
                "chunk_uid": c.get("chunk_uid", -1),
                "doc_id": c.get("doc_id", -1),
                "source": c.get("source", "unknown"),
                "chunk_id": c.get("chunk_id", -1)
            }
            for c in chunks
        ]

        self.add_documents(embeddings, texts, metadata)

        print(f"VectorStore cargado con {len(texts)} documentos desde {path}")

    # -------------------------
    # Search
    # -------------------------
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:

        query_embedding = self._normalize(query_embedding)

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            score = float(distances[0][i])

            if score_threshold is not None and score < score_threshold:
                continue

            results.append({
                "text": self.texts[idx],
                "metadata": self.metadata[idx],  
                "score": score
            })

        return results