import re
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_into_paragraphs(text: str) -> list:
    """
    Divide el texto en párrafos de forma más robusta.
    """
    # Intentar dividir por dobles saltos primero
    paragraphs = re.split(r"\n\s*\n", text)

    # Si no hay suficientes párrafos, fallback a saltos simples
    if len(paragraphs) <= 1:
        paragraphs = text.split("\n")

    # Limpieza básica
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return paragraphs


def split_long_paragraph(paragraph: str, max_size: int) -> list:
    """
    Divide párrafos demasiado largos en segmentos más pequeños.
    """
    if len(paragraph) <= max_size:
        return [paragraph]

    sentences = re.split(r"(?<=[\.\!\?])\s+", paragraph)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) > max_size:
            if current:
                chunks.append(current.strip())
            current = sentence
        else:
            current += " " + sentence if current else sentence

    if current:
        chunks.append(current.strip())

    return chunks


def build_chunks_from_paragraphs(paragraphs: list, chunk_size: int, overlap: int) -> list:
    """
    Construye chunks agrupando párrafos hasta alcanzar el tamaño objetivo.
    Aplica overlap entre chunks a nivel de contenido.
    """
    chunks = []
    current_chunk = ""
    current_length = 0

    i = 0

    while i < len(paragraphs):
        paragraph = paragraphs[i]

        # Si el párrafo es demasiado largo, lo fragmentamos
        sub_paragraphs = split_long_paragraph(paragraph, chunk_size)

        for sub_p in sub_paragraphs:
            para_length = len(sub_p)

            if current_length + para_length > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Overlap basado en caracteres desde el final
                overlap_text = current_chunk[-overlap:] if overlap > 0 else ""
                current_chunk = overlap_text + " " + sub_p
                current_length = len(current_chunk)

            else:
                if current_chunk:
                    current_chunk += " " + sub_p
                else:
                    current_chunk = sub_p

                current_length += para_length

        i += 1

    if current_chunk:
        chunks.append(current_chunk.strip())

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
    import re
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