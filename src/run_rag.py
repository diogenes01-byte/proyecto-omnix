from src.vectorstore.store import VectorStore
from src.rag.pipeline import RAGPipeline

store = VectorStore(embedding_dim=384)
store.load_from_pickle()

rag = RAGPipeline(store)

result = rag.query("where is paris located?")

print(result["answer"])

print("\n--- CONTEXT ---\n")

for i, doc in enumerate(result["context"], 1):
    print(f"[{i}] Score: {doc['score']}")
    print(doc["text"][:300])
    print("-----")