import re
from typing import List, Dict, Any


def normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)   # solo espacios horizontales
    text = re.sub(r"\n{3,}", "\n\n", text)  # preservar párrafos
    return text.strip()


def fix_hyphen_line_breaks(text: str) -> str:
    return re.sub(r"-\s*\n\s*", "", text)


def fix_line_break_words(text: str) -> str:
    # 🔥 Cambio: preservar doble salto de línea (párrafos)
    return re.sub(r"\n(?!\n)", " ", text)


def fix_spaced_letters(text: str) -> str:
    pattern = r"(?:\b(?:[A-Za-z]\s){2,}[A-Za-z]\b)"

    def replace_match(match):
        return match.group(0).replace(" ", "")

    return re.sub(pattern, replace_match, text)


def fix_camel_case_and_joined_words(text: str) -> str:
    return re.sub(
        r"(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])",
        " ",
        text
    )


def remove_pdf_noise(text: str) -> str:
    """
    Versión más conservadora:
    - NO rompe Markdown
    - SOLO elimina ruido muy específico
    """
    text = re.sub(r"/[A-Za-z0-9]{1,4}", " ", text)
    text = re.sub(r"[^\w\s\.\,\;\:\-\(\)\[\]\#\/\:\%\&]", " ", text)
    return text


def clean_text(text: str) -> str:
    if not text:
        return ""

    # 1. Correcciones estructurales
    text = fix_hyphen_line_breaks(text)
    text = fix_line_break_words(text)

    # 2. Reconstrucciones
    text = fix_spaced_letters(text)
    text = fix_camel_case_and_joined_words(text)

    # 3. Limpieza ligera
    text = remove_pdf_noise(text)

    # 4. Normalización final (Markdown-safe)
    text = normalize_whitespace(text)

    return text


def clean_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {**doc, "clean_text": clean_text(doc["text"])}
        for doc in documents
    ]


if __name__ == "__main__":
    from src.ingestion.load_documents import load_documents

    docs = load_documents()

    for doc in docs[:2]:
        print("\nSOURCE:", doc["source"])

        print("\n--- RAW ---")
        print(doc["text"][:300])

        print("\n--- CLEAN ---")
        print(clean_text(doc["text"])[:300])

        print("\n" + "-" * 80)