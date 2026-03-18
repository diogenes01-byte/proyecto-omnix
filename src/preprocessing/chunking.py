from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.ingestion.load_documents import load_pdfs


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def process_documents():
    documents = load_pdfs()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    chunks = process_documents()

    print(f"Total chunks generados: {len(chunks)}\n")

    for c in chunks[:5]:
        print(f"{c['source']} - chunk {c['chunk_id']}")
        print(c["text"][:300])
        print("-" * 50)