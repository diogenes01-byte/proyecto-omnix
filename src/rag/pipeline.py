import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from src.vectorstore.store import VectorStore
from src.config import EMBEDDING_MODEL

load_dotenv()


class RAGPipeline:
    def __init__(self, vector_store: VectorStore, model_name: str = "gpt-4o-mini"):
        self.vector_store = vector_store
        self.client = OpenAI()

        self.embedding_model = EMBEDDING_MODEL
        self.model_name = model_name

    # -------------------------
    # EMBEDDING
    # -------------------------
    def _embed(self, text: str):
        if not text or not text.strip():
            raise ValueError("Input text for embedding is empty.")

        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embedding = np.array(response.data[0].embedding, dtype="float32")

            # Normalizar el embedding para mejorar la similitud coseno
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            return embedding

        except Exception as e:
            raise RuntimeError(f"Embedding failed: {e}")

    # -------------------------
    # RETRIEVAL
    # -------------------------
    def _retrieve(self, query: str, k: int = 5):
        if k <= 0:
            k = 5

        query_embedding = self._embed(query).reshape(1, -1)
        return self.vector_store.search(query_embedding, k=k)

    # -------------------------
    # CONTEXT BUILDER
    # -------------------------
    def _build_context(self, retrieved_docs, max_chars: int = 4000):
        chunks = []
        total_length = 0

        for i, doc in enumerate(retrieved_docs, start=1):
            text = (doc.get("text") or "").strip()
            score = doc.get("score")

            block = f"[Document {i}]\n{text}"

            if score is not None:
                block += f"\nScore: {score:.4f}"

            # Limitar tamaño total
            if total_length + len(block) > max_chars:
                break

            chunks.append(block)
            total_length += len(block)

        return "\n\n".join(chunks)

    # -------------------------
    # SOURCES BUILDER
    # -------------------------
    def _build_sources(self, retrieved_docs):
        sources = []

        for doc in retrieved_docs:
            meta = doc.get("metadata") or {}

            sources.append({
                "chunk_uid": meta.get("chunk_uid", ""),
                "doc_id": meta.get("doc_id", ""),
                "source": meta.get("source", ""),
                "chunk_id": meta.get("chunk_id", ""),
                "text": doc.get("text", "")
            })

        return sources

    # -------------------------
    # PROMPT
    # -------------------------
    def _build_prompt(self, question: str, context: str):
        return f"""
You are a precise and reliable question answering system.

Use ONLY the provided context to answer the question.

If the answer is not in the context, say:
"I don't have enough information in the provided documents."

---

CONTEXT:
{context}

---

QUESTION:
{question}

ANSWER:
""".strip()

    # -------------------------
    # MAIN QUERY
    # -------------------------
    def query(self, question: str, k: int = 5):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        docs = self._retrieve(question, k=k)

        if not docs:
            return {
                "answer": "I don't have enough information in the provided documents.",
                "sources": [],
                "context": []
            }

        context = self._build_context(docs)
        prompt = self._build_prompt(question, context)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            answer = response.choices[0].message.content

        except Exception as e:
            answer = f"Error generating response: {e}"

        return {
            "answer": answer,
            "sources": self._build_sources(docs),
            "context": docs
        }