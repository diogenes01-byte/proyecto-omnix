from src.vectorstore.store import VectorStore
from src.rag.pipeline import RAGPipeline

print("1. cargando vectorstore...")

store = VectorStore(embedding_dim=384)  # ajusta si tu modelo es distinto
store.load_from_pickle("data/embeddings/chunks_embeddings.pkl")

print("2. inicializando pipeline...")

rag = RAGPipeline(vector_store=store)

print("3. haciendo query...")

result = rag.query("what is inflation?", k=5)

print("\n=== ANSWER ===\n")
print(result["answer"])

print("\n=== SOURCES ===\n")
for doc in result["context"]:
    print(doc["score"], doc["text"][:150])
    print("-" * 40)