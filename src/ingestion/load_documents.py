from pypdf import PdfReader
import os
from src.config import RAW_DIR

def load_pdfs():
    documents = []

    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(RAW_DIR, filename)
            reader = PdfReader(filepath)

            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            documents.append({
                "source": filename,
                "text": text
            })

    return documents


if __name__ == "__main__":
    docs = load_pdfs()
    print(f"Total documentos cargados: {len(docs)}\n")

    for doc in docs:
        print(f"Documento: {doc['source']}")
        print(doc["text"][:500])  # preview
        print("-" * 50)
        