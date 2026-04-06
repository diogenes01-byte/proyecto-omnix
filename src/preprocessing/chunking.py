import re
from typing import List, Dict, Any
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


# ---------------------------
# 1. SPLIT POR HEADERS 
# ---------------------------
def split_by_headers(text: str) -> List[str]:
    """
    Divide texto usando headers Markdown (#, ##, ###)
    """
    sections = re.split(r"\n(?=# )|\n(?=## )|\n(?=### )", text)
    return [s.strip() for s in sections if len(s.strip()) > 50]


# ---------------------------
# 2. PÁRRAFOS 
# ---------------------------
def split_into_paragraphs(text: str) -> List[str]:
    paragraphs = re.split(r"\n\s*\n", text)

    if len(paragraphs) <= 1:
        paragraphs = re.split(r'(?<=[.!?])\s+', text)

    return [p.strip() for p in paragraphs if len(p.strip()) > 40]


# ---------------------------
# 3. ORACIONES
# ---------------------------
def split_into_sentences(text: str) -> List[str]:
    return re.split(r'(?<=[.!?])\s+', text)


# ---------------------------
# 4. DIVISIÓN DE BLOQUES LARGOS
# ---------------------------
def split_long_text(text: str, max_size: int) -> List[str]:
    if len(text) <= max_size:
        return [text]

    sentences = split_into_sentences(text)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) > max_size:
            if current:
                chunks.append(current.strip())
                current = sentence
            else:
                chunks.append(sentence[:max_size])
        else:
            current += " " + sentence if current else sentence

    if current:
        chunks.append(current.strip())

    return chunks


# ---------------------------
# 5. OVERLAP LIMPIO
# ---------------------------
def apply_overlap(prev_chunk: str, overlap: int) -> str:
    if overlap <= 0 or len(prev_chunk) <= overlap:
        return ""

    overlap_text = prev_chunk[-overlap:]

    # Evitar cortar palabras
    return re.sub(r'^\S+\s*', '', overlap_text)


# ---------------------------
# 6. PIPELINE PRINCIPAL
# ---------------------------
def build_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks = []

    # 🔥 PRIORIDAD: headers
    sections = split_by_headers(text)

    # fallback si no hay estructura
    if len(sections) <= 1:
        sections = split_into_paragraphs(text)

    current_chunk = ""

    for section in sections:
        sub_chunks = split_long_text(section, chunk_size)

        for sub in sub_chunks:
            if len(current_chunk) + len(sub) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                overlap_text = apply_overlap(current_chunk, overlap)
                current_chunk = (overlap_text + " " + sub).strip() if overlap_text else sub
            else:
                current_chunk += " " + sub if current_chunk else sub

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ---------------------------
# 7. PIPELINE DOCUMENTOS
# ---------------------------
def process_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    all_chunks = []
    chunk_uid_counter = 0

    for doc_id, doc in enumerate(documents):
        text = doc.get("clean_text", "")
        if not text:
            continue

        chunks = build_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            if len(chunk) < 50:  # filtro mínimo simple
                continue

            all_chunks.append({
                "chunk_uid": chunk_uid_counter,
                "doc_id": doc_id,
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk,
                "chunk_length": len(chunk)
            })

            chunk_uid_counter += 1

    return all_chunks


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    from src.ingestion.load_documents import load_documents
    from src.preprocessing.text_cleaner import clean_documents

    docs = load_documents()
    clean_docs = clean_documents(docs)
    chunks = process_documents(clean_docs)

    print(f"Total chunks generados: {len(chunks)}\n")

    for c in chunks[:6]:
        print(f"[{c['chunk_uid']}] {c['source']} - chunk {c['chunk_id']}")
        print(c["text"][:300])
        print("-" * 60)