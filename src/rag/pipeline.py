# src/rag/pipeline.py
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

from openai import OpenAI
from sentence_transformers import SentenceTransformer
from src.vectorstore.store import VectorStore
from src.config import EMBEDDING_MODEL, LLM_MODEL

# Inicializar cliente OpenAI (usa la API key del .env)
client = OpenAI()


class RAGPipeline:

    def __init__(self):
        print("Construyendo índice vectorial...")
        self.vs = VectorStore()
        self.vs.build_index()

        print("Cargando modelo de embeddings...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

    def retrieve(self, query, k=10):
        """Obtiene los k chunks más relevantes del vectorstore"""
        query_embedding = self.embedder.encode([query]).astype("float32")
        results = self.vs.search(query_embedding, k=k)  # devuelve lista de dicts con 'text' y 'metadata'
        return results

    def generate(self, query, context_chunks):
        """Genera la respuesta usando LLM con los chunks proporcionados"""
        # Limpiar saltos de línea y tabs
        context = "\n\n".join([c["text"].replace("\n", " ").replace("\t", " ") for c in context_chunks])

        prompt = f"""
You are an expert in economics and central banking.

Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".
If multiple passages are relevant, synthesize them into a concise answer.

Context:
{context}

Question:
{query}
"""

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    def query(self, question: str, k: int = 5):
        """
        Pipeline completo: búsqueda + generación + retorno de sources
        """
        # 1️⃣ Recuperar los chunks más relevantes
        docs = self.retrieve(question, k=k)

        # 2️⃣ Preparar los sources con metadatos
        sources = []
        for doc in docs:
            metadata = doc.get("metadata", {})
            sources.append({
                "source": metadata.get("source", "unknown"),
                "chunk_id": metadata.get("chunk_id", -1),
                "content": doc["text"][:300]  # opcional: limitar longitud
            })

        # 3️⃣ Generar respuesta con LLM
        answer = self.generate(question, docs)

        # 4️⃣ Retornar resultado completo
        return {
            "query": question,
            "answer": answer,
            "sources": sources
        }


# Ejemplo de uso
if __name__ == "__main__":
    rag = RAGPipeline()

    q = "What is the ECB's view on inflation?"
    result = rag.query(q)

    print("\nPregunta:", result["query"])
    print("\nRespuesta:\n", result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print(f"- {s['source']} (chunk {s['chunk_id']})")