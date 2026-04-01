from src.vectorstore.store import VectorStore
from src.rag.pipeline import RAGPipeline
from src.config import EMBEDDING_DIM

print("1. cargando vectorstore...")

# Usa dimensión desde config (1536)
store = VectorStore(embedding_dim=EMBEDDING_DIM)
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