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

        # OpenAI embedding model
        self.embedding_model = EMBEDDING_MODEL

        self.model_name = model_name

    # -------------------------
    # EMBEDDING (OPENAI ONLY)
    # -------------------------
    def _embed(self, text: str):
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return np.array(response.data[0].embedding, dtype="float32")

    # -------------------------
    # RETRIEVAL
    # -------------------------
    def _retrieve(self, query: str, k: int = 5):
        query_embedding = self._embed(query).reshape(1, -1)
        return self.vector_store.search(query_embedding, k=k)

    # -------------------------
    # CONTEXT BUILDER
    # -------------------------
    def _build_context(self, retrieved_docs):
        chunks = []

        for i, doc in enumerate(retrieved_docs, start=1):
            text = doc["text"].strip()
            score = doc.get("score", None)

            block = f"[Document {i}]\n{text}"

            if score is not None:
                block += f"\nScore: {score:.4f}"

            chunks.append(block)

        return "\n\n".join(chunks)

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
        docs = self._retrieve(question, k=k)
        context = self._build_context(docs)
        prompt = self._build_prompt(question, context)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return {
            "answer": response.choices[0].message.content,
            "context": docs
        }