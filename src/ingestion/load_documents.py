import os
import re
from pypdf import PdfReader
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


def read_pdf(filepath: str) -> dict:
    """
    Lee un PDF página por página:
    - maneja errores por página
    - concatena texto
    - devuelve metadatos útiles
    """
    reader = PdfReader(filepath)
    text = ""
    failed_pages = 0

    for i, page in enumerate(reader.pages):
        try:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
            else:
                failed_pages += 1
        except Exception:
            failed_pages += 1

    return {
        "text": clean_text(text),
        "num_pages": len(reader.pages),
        "failed_pages": failed_pages
    }


def load_pdfs():
    """
    Carga todos los PDFs desde RAW_DIR:
    - ordena archivos (consistencia)
    - ignora documentos vacíos
    - añade metadatos para RAG
    """
    documents = []

    for idx, filename in enumerate(sorted(os.listdir(RAW_DIR))):
        if filename.endswith(".pdf"):
            filepath = os.path.join(RAW_DIR, filename)

            pdf_data = read_pdf(filepath)

            # Validación: ignorar PDFs sin texto
            if not pdf_data["text"]:
                print(f"[WARNING] Documento vacío ignorado: {filename}")
                continue

            documents.append({
                "doc_id": idx,
                "source": filename,
                "path": filepath,
                "num_pages": pdf_data["num_pages"],
                "failed_pages": pdf_data["failed_pages"],
                "text": pdf_data["text"]
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