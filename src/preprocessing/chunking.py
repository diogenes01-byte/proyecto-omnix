import re
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


# ---------------------------
# 1. PÁRRAFOS
# ---------------------------
def split_into_paragraphs(text: str) -> list:
    paragraphs = re.split(r"\n\s*\n", text)

    if len(paragraphs) <= 1:
        paragraphs = re.split(r'(?<=[.!?])\s+', text)

    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 40]

    return paragraphs


# ---------------------------
# 2. SPLIT POR ORACIONES
# ---------------------------
def split_into_sentences(text: str) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def split_long_paragraph(paragraph: str, max_size: int) -> list:
    if len(paragraph) <= max_size:
        return [paragraph]

    sentences = split_into_sentences(paragraph)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 > max_size:
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
# 3. DETECCIÓN DE FINAL DE ORACIÓN
# ---------------------------
def get_sentence_boundaries(text: str) -> list:
    return [m.end() for m in re.finditer(r'[.!?]\s+', text)]


# ---------------------------
# 4. VALIDACIÓN DE CHUNKS
# ---------------------------
def is_valid_chunk(text: str) -> bool:
    if len(text) < 80:
        return False

    if not re.search(
        r"\b(is|are|was|were|be|have|has|had|increase|decrease|shows|find)\b",
        text,
        re.IGNORECASE,
    ):
        return False

    return True


# ---------------------------
# 5. CONSTRUCCIÓN DE CHUNKS
# ---------------------------
def build_chunks_from_paragraphs(paragraphs: list, chunk_size: int, overlap: int) -> list:
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        sub_paragraphs = split_long_paragraph(paragraph, chunk_size)

        for sub_p in sub_paragraphs:
            if len(current_chunk) + len(sub_p) > chunk_size and current_chunk:

                boundaries = get_sentence_boundaries(current_chunk)

                if boundaries:
                    target = min(len(current_chunk), chunk_size)
                    cut_pos = max([b for b in boundaries if b <= target] or [target])
                    final_chunk = current_chunk[:cut_pos].strip()
                else:
                    final_chunk = current_chunk.strip()

                if is_valid_chunk(final_chunk):
                    chunks.append(final_chunk)

                overlap_text = ""
                if overlap > 0 and len(current_chunk) > overlap:
                    overlap_text = current_chunk[-overlap:]
                    overlap_text = re.sub(r'^\S+\s*', '', overlap_text)

                current_chunk = (overlap_text + " " + sub_p).strip() if overlap_text else sub_p

            else:
                current_chunk += " " + sub_p if current_chunk else sub_p

    if current_chunk and is_valid_chunk(current_chunk):
        chunks.append(current_chunk.strip())

    return chunks


# ---------------------------
# 6. PIPELINE FINAL
# ---------------------------
def process_documents(documents: list) -> list:
    all_chunks = []
    chunk_uid_counter = 0  # 🔥 NUEVO: ID global

    for doc_id, doc in enumerate(documents):
        text = doc.get("clean_text", "")
        if not text:
            continue

        paragraphs = split_into_paragraphs(text)
        chunks = build_chunks_from_paragraphs(paragraphs, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_uid": chunk_uid_counter,   # 🔥 NUEVO (GLOBAL UNIQUE ID)
                "doc_id": doc_id,
                "source": doc["source"],
                "chunk_id": i,                    # local por documento
                "text": chunk,
                "chunk_length": len(chunk)
            })

            chunk_uid_counter += 1

    return all_chunks


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    from src.ingestion.load_documents import load_pdfs
    from src.preprocessing.text_cleaner import clean_documents

    docs = load_pdfs()
    clean_docs = clean_documents(docs)
    chunks = process_documents(clean_docs)

    print(f"Total chunks generados: {len(chunks)}\n")

    for c in chunks[:6]:
        print(f"[{c['chunk_uid']}] {c['source']} - chunk {c['chunk_id']}")
        print(c["text"][:300])
        print("-" * 60)