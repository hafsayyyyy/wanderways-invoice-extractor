from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from all pages of a PDF invoice.
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    text_parts = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)