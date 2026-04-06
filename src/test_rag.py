from src.vectorstore.store import VectorStore
from src.rag.pipeline import RAGPipeline
from src.config import EMBEDDING_DIM


def main():
    try:
        # Inicializar store
        store = VectorStore(embedding_dim=EMBEDDING_DIM)
        store.load_from_pickle()

        if not store.texts:
            print("⚠️ Vector store está vacío.")
            return

        # Inicializar RAG
        rag = RAGPipeline(store)

        # -------------------------
        # LISTA DE PREGUNTAS
        # -------------------------
        questions = [
            "what is inflation?",
            "what is the capital of Venezuela?"
        ]

        # -------------------------
        # LOOP DE TESTS
        # -------------------------
        for idx, question in enumerate(questions, 1):

            print("\n" + "=" * 60)
            print(f"TEST {idx}")
            print(f"QUESTION: {question}")
            print("=" * 60)

            result = rag.query(question, k=5)

            # -------------------------
            # ANSWER
            # -------------------------
            print("\n=== ANSWER ===\n")
            print(result.get("answer", ""))

            # -------------------------
            # CONTEXT
            # -------------------------
            print("\n=== CONTEXT ===\n")

            for i, doc in enumerate(result.get("context", []), 1):
                score = doc.get("score", "N/A")
                text = (doc.get("text") or "")[:300]

                print(f"[{i}] Score: {score}")
                print(text)
                print("-----")

            # -------------------------
            # SOURCES
            # -------------------------
            print("\n=== SOURCES ===\n")

            for s in result.get("sources", []):
                print(s)

        print("\n✔️ TEST COMPLETED")

    except Exception as e:
        print(f"❌ Error en test RAG: {e}")


if __name__ == "__main__":
    main()