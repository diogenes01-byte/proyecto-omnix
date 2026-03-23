from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_into_paragraphs(text: str) -> list:
    """
    Divide el texto en párrafos usando saltos de línea.
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return paragraphs


def build_chunks_from_paragraphs(paragraphs: list, chunk_size: int, overlap: int) -> list:
    """
    Construye chunks agrupando párrafos hasta alcanzar el tamaño objetivo.
    Aplica overlap entre chunks a nivel de párrafos.
    """
    chunks = []
    current_chunk = []
    current_length = 0

    i = 0

    while i < len(paragraphs):
        paragraph = paragraphs[i]
        para_length = len(paragraph)

        # Si añadir este párrafo excede el tamaño, cerramos chunk actual
        if current_length + para_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))

            # Aplicar overlap: retroceder algunos párrafos
            overlap_paragraphs = []
            overlap_length = 0

            for p in reversed(current_chunk):
                if overlap_length >= overlap:
                    break
                overlap_paragraphs.insert(0, p)
                overlap_length += len(p)

            current_chunk = overlap_paragraphs
            current_length = overlap_length

        else:
            current_chunk.append(paragraph)
            current_length += para_length
            i += 1

    # Añadir último chunk si existe
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def process_documents(documents: list) -> list:
    """
    Recibe documentos ya limpios (con 'clean_text')
    y devuelve chunks con metadata.
    """
    all_chunks = []

    for doc_id, doc in enumerate(documents):
        text = doc.get("clean_text", "")

        if not text:
            continue

        paragraphs = split_into_paragraphs(text)
        chunks = build_chunks_from_paragraphs(paragraphs, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "doc_id": doc_id,
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk,
                "chunk_length": len(chunk)
            })

    return all_chunks


if __name__ == "__main__":
    # Test manual (requiere conectar con ingestion + cleaning)
    from src.ingestion.load_documents import load_pdfs
    from src.preprocessing.text_cleaner import clean_documents

    docs = load_pdfs()
    clean_docs = clean_documents(docs)

    chunks = process_documents(clean_docs)

    print(f"Total chunks generados: {len(chunks)}\n")

    for c in chunks[:5]:
        print(f"{c['source']} - chunk {c['chunk_id']}")
        print(c["text"][:300])
        print("-" * 50)