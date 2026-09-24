# WanderWays Invoice Extractor

Task 2 implements reusable LLM-based extraction for travel invoice PDFs. The project follows the brief: extract PDF text, apply a reusable prompt and JSON schema, call the OpenAI API, validate the response, and return a predictable JSON object.

## Extracted fields

- `invoice_date`
- `total_amount`
- `vendor_name`
- `travel_dates`
- `booking_reference`

## Project Structure

- `src/pdf_extractor.py` - PDF-to-text extraction with PyPDF2
- `src/invoice_extractor.py` - prompt, OpenAI API call, JSON parsing, validation, and fallback handling
- `src/invoice_schema.json` - JSON Schema used by the model and jsonschema validator
- `prompts/invoice_extraction_prompt.txt` - reusable extraction prompt
- `tests/test_invoice_extractor.py` - pytest tests
- `samples/` - London, Dubai, and Istanbul sample invoices
- `.env.example` - required environment variable template

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
py -m venv .venv
.venv\\Scripts\\activate
py -m pip install -r requirements.txt
```

Set your API key in the environment:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_MODEL="gpt-4o-mini"
```

The API key must remain private and must never be committed to GitHub.

## Run

Process a PDF:

```bash
py -m src.main samples/london_invoice.pdf
```

The program returns JSON such as:

```json
{
  "invoice_date": "2024-08-15",
  "total_amount": 1234.56,
  "vendor_name": "Acme Travel",
  "travel_dates": ["2024-09-01", "2024-09-10"],
  "booking_reference": "ABC123"
}
```

## Test

Run the deterministic unit tests:

```bash
py -m pytest -q
```

The tests use the real London sample PDF for the PDF extraction path and mock the API response so tests do not spend API credits. A separate test verifies the user-friendly fallback when the API fails.

## Task 2 completion note

I implemented a reusable invoice-extraction prompt and matching JSON Schema, connected PDF text extraction to the OpenAI API, validated model output, and added error logging with a safe JSON fallback. The main challenge was keeping the model response strictly schema-compliant while making tests repeatable without requiring a live API call. Live API execution requires a valid OpenAI API key and was intentionally kept out of automated tests.
