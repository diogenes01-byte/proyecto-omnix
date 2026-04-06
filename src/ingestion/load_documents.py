import os
import re
import logging
from typing import Dict, Any, List
from src.config import RAW_DIR

logging.basicConfig(level=logging.INFO)


def clean_text(text: str) -> str:
    """
    Limpia el texto:
    - elimina saltos de línea excesivos
    - elimina espacios duplicados
    """
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_md(filepath: str) -> Dict[str, Any]:
    """
    Lee un archivo Markdown y devuelve texto limpio
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        logging.warning(f"Error leyendo archivo {filepath}: {e}")
        text = ""

    return {
        "text": clean_text(text),
        "num_pages": 1,
        "failed_pages": 0
    }


def load_documents() -> List[Dict[str, Any]]:
    """
    Carga todos los archivos .md desde RAW_DIR
    """
    documents = []

    if not os.path.exists(RAW_DIR):
        logging.error(f"Directorio no encontrado: {RAW_DIR}")
        return documents

    for idx, filename in enumerate(sorted(os.listdir(RAW_DIR))):
        if filename.endswith(".md"):
            filepath = os.path.join(RAW_DIR, filename)

            md_data = read_md(filepath)

            if not md_data["text"]:
                logging.warning(f"Documento vacío ignorado: {filename}")
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
    docs = load_documents()

    logging.info(f"Total documentos cargados: {len(docs)}")

    for doc in docs:
        logging.info(f"Documento: {doc['source']}")
        logging.info(f"Páginas: {doc['num_pages']} | Fallidas: {doc['failed_pages']}")
        print(doc["text"][:500])
        print("-" * 50)