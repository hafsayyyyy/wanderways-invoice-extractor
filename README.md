# WanderWays Invoice Extractor

WanderWays Invoice Extractor is an LLM-based system for extracting structured information from travel invoice PDFs. The project extracts PDF text, applies a reusable prompt and JSON Schema, sends the information to the OpenAI API, validates the extracted data, and returns a predictable JSON result.

The project also provides a Flask-based web interface where users can upload PDF invoices directly through a browser.

## Extracted Fields

The system extracts the following invoice information:

- `invoice_date`
- `total_amount`
- `vendor_name`
- `travel_dates`
- `booking_reference`

Additional invoice fields such as `invoice_number` and return date are also supported by the validation layer.

## Features

- PDF-to-text extraction
- Reusable LLM extraction prompt
- JSON Schema-based structured output
- OpenAI API integration
- Invoice data validation
- ISO date validation
- Numeric amount validation
- Empty vendor name validation
- Travel date range validation
- Clear validation error messages
- Safe fallback when extraction fails
- Flask web interface
- Browser-based PDF upload
- Temporary file handling
- Automated pytest tests
- Sample travel invoices for testing

## Project Structure

```text
wanderways-invoice-extractor/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── prompts/
│   └── invoice_extraction_prompt.txt
│
├── samples/
│   ├── london_invoice.pdf
│   ├── dubai_invoice.pdf
│   └── istanbul_invoice.pdf
│
├── src/
│   ├── pdf_extractor.py
│   ├── invoice_extractor.py
│   ├── invoice_schema.json
│   └── validator.py
│
├── templates/
│   └── index.html
│
└── tests/
    ├── test_invoice_extractor.py
    └── test_validator.py