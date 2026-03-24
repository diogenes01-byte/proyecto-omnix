import faiss
import numpy as np
import pickle
from typing import List, Dict, Any, Optional

from sentence_transformers import CrossEncoder

# RUTA DESDE CONFIG
from src.config import EMBEDDINGS_FILE


class VectorStore:
    def __init__(
        self,
        embedding_dim: int,
        use_reranker: bool = False,
        reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        # FAISS index (cosine similarity via inner product after normalization)
        self.index = faiss.IndexFlatIP(embedding_dim)

        self.texts: List[str] = []
        self.metadata: List[Dict[str, Any]] = []

        # Reranker opcional
        self.use_reranker = use_reranker
        self.reranker = CrossEncoder(reranker_model) if use_reranker else None

    # -------------------------
    # Utilities
    # -------------------------
    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
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
    # Load from pickle (NEW)
    # -------------------------
    def load_from_pickle(self, path: str = EMBEDDINGS_FILE):
        """
        Carga embeddings, textos y metadata desde el .pkl generado por el embedder
        """
        with open(path, "rb") as f:
            chunks = pickle.load(f)

        if not chunks:
            raise ValueError("El archivo pickle está vacío")

        # Extraer datos
        embeddings = np.array([c["embedding"] for c in chunks]).astype("float32")
        texts = [c["text"] for c in chunks]
        metadata = [c.get("metadata", {}) for c in chunks]

        # Cargar en FAISS
        self.add_documents(embeddings, texts, metadata)

        print(f"✅ VectorStore cargado con {len(texts)} documentos desde {path}")

    # -------------------------
    # Search with scores
    # -------------------------
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        score_threshold: Optional[float] = None,
        rerank: bool = False
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