from pathlib import Path
from unittest.mock import MagicMock

from jsonschema import validate

from src.invoice_extractor import FALLBACK_RESULT, extract_invoice_data, load_schema

SAMPLE_PDF = Path(__file__).parents[1] / "samples" / "london_invoice.pdf"

def test_sample_invoice_pdf_extraction():
    """Feed the real London sample PDF through the extraction function."""
    fake_response = MagicMock()
    fake_response.choices[0].message.content = (
        '{"invoice_date":"2024-08-15","total_amount":1234.56,'
        '"vendor_name":"Acme Travel","travel_dates":["2024-09-01","2024-09-10"],'
        '"booking_reference":"ABC123"}'
    )
    client = MagicMock()
    client.chat.completions.create.return_value = fake_response

    result = extract_invoice_data(SAMPLE_PDF, client=client)

    expected = {
        "invoice_date": "2024-08-15",
        "total_amount": 1234.56,
        "vendor_name": "Acme Travel",
        "travel_dates": ["2024-09-01", "2024-09-10"],
        "booking_reference": "ABC123",
    }
    assert result == expected
    validate(instance=result, schema=load_schema())
    client.chat.completions.create.assert_called_once()

def test_api_error_returns_user_friendly_fallback():
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError("API unavailable")

    from src.invoice_extractor import extract_invoice_data_from_text
    result = extract_invoice_data_from_text("Invoice text", client=client)

    assert result == FALLBACK_RESULT
