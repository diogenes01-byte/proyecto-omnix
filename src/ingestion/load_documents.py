import os
import re
from src.config import RAW_DIR


def clean_text(text: str) -> str:
    """
    Limpia el texto:
    - elimina saltos de línea excesivos
    - elimina espacios duplicados
    """
    text = re.sub(r"\n+", "\n", text)        # múltiples saltos → uno
    text = re.sub(r"\s+", " ", text)         # múltiples espacios → uno
    return text.strip()


def read_md(filepath: str) -> dict:
    """
    Lee un archivo Markdown:
    - devuelve texto limpio
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        text = ""

    return {
        "text": clean_text(text),
        "num_pages": 1,        # placeholder para mantener compatibilidad
        "failed_pages": 0
    }


def load_pdfs():
    """
    Carga todos los archivos .md desde RAW_DIR:
    - ordena archivos (consistencia)
    - ignora documentos vacíos
    - añade metadatos para RAG
    """
    documents = []

    for idx, filename in enumerate(sorted(os.listdir(RAW_DIR))):
        if filename.endswith(".md"):
            filepath = os.path.join(RAW_DIR, filename)

            md_data = read_md(filepath)

            # Validación: ignorar documentos vacíos
            if not md_data["text"]:
                print(f"[WARNING] Documento vacío ignorado: {filename}")
                continue

            documents.append({
                "doc_id": idx,
                "source": filename,
                "path": filepath,
                "num_pages": md_data["num_pages"],
                "failed_pages": md_data["failed_pages"],
                "text": md_data["text"]
            })

    return documents


if __name__ == "__main__":
    docs = load_pdfs()

    print(f"\nTotal documentos cargados: {len(docs)}\n")

    for doc in docs:
        print(f"Documento: {doc['source']}")
        print(f"Páginas: {doc['num_pages']} | Fallidas: {doc['failed_pages']}")
        print(doc["text"][:500])  # preview
        print("-" * 50)