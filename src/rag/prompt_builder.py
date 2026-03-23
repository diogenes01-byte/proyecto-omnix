from typing import List, Dict


class PromptBuilder:

    def __init__(self):
        pass

    def build_context(self, docs: List[Dict]) -> str:
        """
        Convierte los documentos recuperados en un contexto estructurado con citations.
        Cada chunk se etiqueta como [1], [2], etc.
        """

        formatted_chunks = []

        for i, doc in enumerate(docs):
            text = doc.get("text", "").replace("\n", " ").replace("\t", " ")
            formatted_chunks.append(f"[{i+1}] {text}")

        return "\n\n".join(formatted_chunks)

    def build_prompt(self, query: str, docs: List[Dict]) -> str:
        """
        Construye el prompt completo para el LLM incluyendo contexto y pregunta.
        """

        context = self.build_context(docs)

        prompt = f"""
You are an expert in economics and central banking.

Answer the question using ONLY the context below.

- Do not mention citations or reference numbers.
- Do not say where the information comes from.
- If the answer is not in the context, say "I don't know".
- Synthesize information when multiple sources are relevant.

Context:
{context}

Question:
{query}

Answer:
"""

        return prompt
    

# -------------------------
# Test rápido en consola      
# -------------------------

if __name__ == "__main__":
    from src.rag.retriever import Retriever

    retriever = Retriever()

    query = "What is inflation?"
    docs = retriever.retrieve(query, k=3)

    builder = PromptBuilder()
    prompt = builder.build_prompt(query, docs)

    print("\n--- PROMPT GENERADO ---\n")
    print(prompt)