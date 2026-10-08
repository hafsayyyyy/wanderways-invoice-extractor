# WanderWays Invoice Extractor

WanderWays Invoice Extractor is an LLM-assisted Flask web application for extracting structured information from travel invoice PDFs and validating the extracted data.

Users can upload a PDF through a browser. The backend extracts the PDF text, sends it through the existing invoice extraction pipeline, validates the resulting data, and displays the extracted fields and validation errors in a readable table.

## Features

- PDF-to-text extraction with PyPDF2.
- Reusable invoice extraction prompt.
- OpenAI API integration.
- JSON Schema-based structured extraction.
- Invoice validation with clear error messages.
- ISO date validation.
- Travel-date range validation.
- Vendor-name validation.
- Numeric total validation.
- Safe extraction fallback when processing fails.
- Flask browser interface.
- PDF upload form.
- Results displayed in an HTML table.
- Validation errors displayed separately.
- Temporary upload files cleaned after processing.
- Pytest test suite.
- Dockerfile and .dockerignore.
- Render free-tier deployment configuration.
- Gunicorn production WSGI server.
- Environment-variable configuration.

## Extracted Information

The extraction pipeline supports fields including:

- invoice_date
- total_amount
- vendor_name
- travel_dates
- booking_reference
- invoice_number
- return_date

The exact fields returned depend on the extraction schema and invoice content.

## Architecture

The web layer is intentionally thin:

1. User uploads a PDF.
2. Flask validates that the uploaded file is a PDF.
3. The PDF is saved temporarily.
4. The existing invoice extractor processes the PDF.
5. The validator checks the extracted data.
6. Flask returns JSON containing extracted data and validation errors.
7. The browser renders the results in a table.
8. The temporary PDF is deleted.

## Project Structure

    wanderways-invoice-extractor/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    ├── .dockerignore
    ├── Dockerfile
    ├── render.yaml
    ├── deploy_render.sh
    ├── HANDOVER.md
    ├── README.md
    ├── prompts/
    │   └── invoice_extraction_prompt.txt
    ├── samples/
    │   ├── london_invoice.pdf
    │   ├── dubai_invoice.pdf
    │   └── istanbul_invoice.pdf
    ├── src/
    │   ├── pdf_extractor.py
    │   ├── invoice_extractor.py
    │   ├── invoice_schema.json
    │   └── validator.py
    ├── templates/
    │   └── index.html
    └── tests/
        ├── test_invoice_extractor.py
        └── test_validator.py

## Requirements

- Python 3.11 or compatible Python 3 version.
- OpenAI API key with available API credits.
- Internet connection for OpenAI API calls.
- Optional: Docker Desktop for container testing.
- Optional: Render account for hosted deployment.

## Local Setup

### 1. Clone the repository

    git clone https://github.com/hafsayyyyy/wanderways-invoice-extractor.git
    cd wanderways-invoice-extractor

### 2. Create a virtual environment

Windows PowerShell:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1

### 3. Install dependencies

    py -m pip install -r requirements.txt

### 4. Configure environment variables

Create a .env file in the project root:

    OPENAI_API_KEY=your_api_key_here
    OPENAI_MODEL=gpt-4o-mini

Never commit the real API key to GitHub.

### 5. Run tests

    py -m pytest

### 6. Start Flask

    py app.py

Open:

    http://127.0.0.1:5000

## Web App Usage

1. Open the Flask URL in a browser.
2. Choose a travel invoice PDF.
3. Click Extract Invoice.
4. Wait for extraction and validation.
5. Review the extracted values in the table.
6. If validation fails, review the validation errors shown below the table.

The API endpoint is also available at:

    POST /extract

Example PowerShell request:

    curl.exe -X POST -F "file=@samples\london_invoice.pdf" http://127.0.0.1:5000/extract

## Error Handling

The application handles:

- Missing file uploads.
- Empty file selection.
- Non-PDF uploads.
- Extraction failures.
- Missing or invalid OpenAI configuration.
- Validation failures.
- Temporary-file cleanup failures.

The application returns HTTP 400 for invalid upload requests and HTTP 500 when invoice processing/extraction cannot be completed.

## Validation Rules

The validation layer checks:

- Required invoice fields.
- Travel and return dates use YYYY-MM-DD.
- Travel date is not after return date.
- Vendor name is not empty.
- Total amount is numeric.
- Input must be a JSON object.

Validation errors are returned in the validation_errors response field and displayed by the browser interface.

## Docker

The repository includes a Dockerfile based on Python 3.11 slim.

Build:

    docker build -t wanderways-invoice-extractor .

Run:

    docker run --rm -p 5000:5000 --env-file .env wanderways-invoice-extractor

Then open:

    http://127.0.0.1:5000

The Docker image uses Gunicorn-compatible dependencies, while the default Docker command starts the Flask application. Docker runtime verification remains pending because Docker Desktop could not start on the development machine.

## Render Free-Tier Deployment

The repository includes render.yaml for a repeatable Render deployment configuration.

### Deployment steps

1. Push the repository to GitHub.
2. Sign in to Render.
3. Create a Blueprint/Web Service from the GitHub repository.
4. Use the repository's render.yaml configuration.
5. Add OPENAI_API_KEY as a secret environment variable.
6. Keep OPENAI_MODEL as gpt-4o-mini unless another supported model is required.
7. Deploy the service.
8. Open the generated service URL.
9. Upload one of the sample invoices and verify the extracted table and validation messages.

The Render start command is:

    gunicorn app:app

The application reads the PORT environment variable supplied by the hosting platform.

## Deployment Helper

deploy_render.sh performs a simple deployment-preparation flow:

1. Installs requirements.
2. Runs pytest.
3. Starts Gunicorn.

Render itself can use render.yaml for the hosted build/start configuration.

## Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| OPENAI_API_KEY | Yes | Authenticates OpenAI API requests. |
| OPENAI_MODEL | No | Selects the OpenAI model. Defaults to gpt-4o-mini. |
| PORT | No | Hosting platform port; defaults to 5000 locally. |
| FLASK_DEBUG | No | Enables Flask debug mode only when explicitly set to 1. |

## Testing

Run the complete test suite:

    py -m pytest

The project includes tests for invoice extraction behavior and invoice validation.

For a hosted deployment, also perform a manual smoke test by uploading a sample PDF through the browser.

## Security and Privacy Notes

- Do not commit .env or API keys.
- Uploaded PDFs are stored temporarily during processing and deleted afterward.
- The current application does not provide authentication.
- The current application does not provide persistent invoice storage.
- For production use with private invoices, add authentication, upload-size limits, stronger content validation, logging, and appropriate data-retention controls.

## Limitations

- OpenAI API access and available credits are required for extraction.
- Extraction quality depends on the source PDF and model response.
- Scanned/image-only PDFs may require OCR support.
- Docker runtime verification could not be completed on the development machine because Docker Desktop would not start.
- Render free-tier availability and limits are controlled by the hosting provider.
- No database or invoice history is included.

## Handover

See HANDOVER.md for:

- Implementation summary.
- Decision log.
- Sample usage.
- Deployment notes.
- Verification status.
- Known limitations.
- Recommended next steps.
- Sign-off information.

## Recommended Next Steps

1. Verify the Docker image on a working Docker runtime or CI environment.
2. Deploy the application to Render and perform a smoke test.
3. Add Flask route tests using the Flask test client.
4. Add upload-size and PDF-content checks.
5. Add authentication before handling private customer invoices.
6. Add structured logging and monitoring.
7. Add CI to run pytest on every push.
8. Add OCR if scanned invoices must be supported.
