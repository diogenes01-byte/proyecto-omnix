import os
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from src.vectorstore.store import VectorStore
from src.config import EMBEDDING_MODEL

from openai import OpenAI

# Cargar variables de entorno
load_dotenv()


class RAGPipeline:
    def __init__(self, vector_store: VectorStore, model_name: str = "gpt-4o-mini"):
        self.vector_store = vector_store
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

        # Cliente OpenAI usa automáticamente OPENAI_API_KEY del entorno
        self.client = OpenAI()

        self.model_name = model_name

    def _retrieve(self, query: str, k: int = 5):
        query_embedding = self.embedder.encode([query]).astype("float32")
        results = self.vector_store.search(query_embedding, k=k)
        return results

    def _build_context(self, retrieved_docs):
        """
        Construye un contexto estructurado y numerado para mejorar la interpretación del LLM.
        """
        formatted_chunks = []

        for i, doc in enumerate(retrieved_docs, start=1):
            text = doc["text"].strip()
            score = doc.get("score", None)

            chunk = f"[Document {i}]\n{text}"

            if score is not None:
                chunk += f"\n(Relevance score: {score:.4f})"

            formatted_chunks.append(chunk)

        return "\n\n".join(formatted_chunks)

    def _build_prompt(self, query: str, context: str):
        return f"""
    You are a question answering system that must answer using the provided documents.

    INSTRUCTIONS:
    - Use the context to synthesize an answer.
    - Do NOT require an exact sentence definition in the context.
    - If the context contains relevant information, infer and summarize it.
    - Only say "I don't know based on the provided documents." if the context is completely unrelated.
    - Be concise but informative.

    CONTEXT:
    ---------------------
    {context}
    ---------------------

    QUESTION:
    {query}

    ANSWER:
    """.strip()

    def query(self, question: str, k: int = 5, rerank: bool = False):
        # Retrieval
        docs = self._retrieve(question, k=k)

        # Context
        context = self._build_context(docs)

        # Prompt
        prompt = self._build_prompt(question, context)

        # LLM call
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