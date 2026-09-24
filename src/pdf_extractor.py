from pathlib import Path
from PyPDF2 import PdfReader

def extract_pdf_text(pdf_path: str | Path) -> str:
    """Extract plain text from every page of a PDF."""
    reader = PdfReader(str(pdf_path))
    text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    if not text:
        raise ValueError("No text could be extracted from the PDF.")
    return text
