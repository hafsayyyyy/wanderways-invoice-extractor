import json
import logging
import os
from pathlib import Path

from jsonschema import validate
from openai import OpenAI

from .pdf_extractor import extract_pdf_text

LOGGER = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR.parent / "prompts" / "invoice_extraction_prompt.txt"
SCHEMA_PATH = BASE_DIR / "invoice_schema.json"

FALLBACK_RESULT = {
    "invoice_date": None,
    "total_amount": None,
    "vendor_name": None,
    "travel_dates": [],
    "booking_reference": None,
}

def load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)

def build_prompt(pdf_text: str) -> str:
    return PROMPT_PATH.read_text(encoding="utf-8").format(text=pdf_text)

def _clean_json_response(content: str) -> dict:
    content = content.strip()
    fence = chr(96) * 3
    if content.startswith(fence):
        content = content[len(fence):].strip()
        if content.lower().startswith("json"):
            content = content[4:].strip()
        if content.endswith(fence):
            content = content[:-len(fence)].strip()
    return json.loads(content)

def _call_model(prompt: str, client: OpenAI) -> dict:
    schema = load_schema()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Return only valid JSON matching the requested invoice schema."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "travel_invoice",
                "strict": True,
                "schema": schema,
            },
        },
    )
    result = _clean_json_response(response.choices[0].message.content or "")
    validate(instance=result, schema=schema)
    return result

def extract_invoice_data(pdf_path: str | Path, client: OpenAI | None = None) -> dict:
    """Extract structured invoice data from an uploaded PDF."""
    try:
        pdf_text = extract_pdf_text(pdf_path)
        client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return _call_model(build_prompt(pdf_text), client)
    except Exception as exc:
        LOGGER.exception("Invoice extraction failed: %s", exc)
        return dict(FALLBACK_RESULT)

def extract_invoice_data_from_text(pdf_text: str, client: OpenAI | None = None) -> dict:
    """Extract structured data from text; useful for deterministic unit tests."""
    try:
        client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return _call_model(build_prompt(pdf_text), client)
    except Exception as exc:
        LOGGER.exception("Invoice text extraction failed: %s", exc)
        return dict(FALLBACK_RESULT)
