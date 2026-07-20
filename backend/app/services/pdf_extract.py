"""
Extracts text page-by-page so outline items / flashcards can reference a
page number the same way video items reference a timestamp. This mirrors
the {start, end, text} shape from transcription.py on purpose — it lets
Hour 13's chunking code treat both source types uniformly.
"""
import pdfplumber


def extract_pdf_pages(file_path: str) -> list[dict]:
    """
    Returns [{"page": int, "text": str}, ...]
    """
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"page": i, "text": text.strip()})
    return pages


def pages_to_full_text(pages: list[dict]) -> str:
    return "\n\n".join(p["text"] for p in pages if p["text"])