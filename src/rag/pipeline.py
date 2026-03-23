from src.rag.retriever import Retriever
from src.rag.prompt_builder import PromptBuilder
from src.rag.generator import Generator


class RAGPipeline:

    def __init__(self):
        print("Inicializando RAG Pipeline...")

        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.generator = Generator()

    def query(self, question: str, k: int = 5):
        """
        Pipeline completo:
        1. Recuperar documentos
        2. Construir prompt
        3. Generar respuesta
        4. Devolver respuesta + fuentes
        """

        # 🔹 1. Retrieval
        docs = self.retriever.retrieve(question, k=k)

        # 🔹 2. Prompt
        prompt = self.prompt_builder.build_prompt(question, docs)

        # 🔹 3. Generación
        answer = self.generator.generate(prompt)

        # 🔹 4. Formatear fuentes (para el usuario)
        sources = []
        for doc in docs:
            metadata = doc.get("metadata", {})
            sources.append({
                "source": metadata.get("source", "unknown"),
                "chunk_id": metadata.get("chunk_id", -1),
                "content": doc["text"][:200]
            })

        return {
            "query": question,
            "answer": answer,
            "sources": sources
        }


# -------------------------
# Test en consola
# -------------------------
if __name__ == "__main__":
    rag = RAGPipeline()

    q1 = "What is inflation?"
    result = rag.query(q1)

    print("\n--- RESPUESTA ---\n")
    print(result["answer"])

    print("\n--- FUENTES ---\n")
    for s in result["sources"]:
        print(f"- {s['source']} (chunk {s['chunk_id']})")
        print(f"  {s['content']}\n")