# WanderWays Invoice Extractor — Handover Note

## 1. Project Summary
This project provides a small Flask web application for uploading travel invoice PDFs. The backend extracts invoice information through the existing PDF/LLM pipeline, validates the extracted data, and returns the results to the browser.

## 2. Implemented Scope
- PDF upload through a browser form.
- Flask routes for the web page and extraction endpoint.
- Temporary PDF storage with cleanup after processing.
- Invoice extraction using the existing OpenAI-based extractor.
- Invoice validation with clear validation errors.
- Browser table showing extracted fields.
- Validation-error display.
- JSON API response from /extract.
- Dockerfile and .dockerignore.
- Render free-tier deployment configuration in render.yaml.
- Production WSGI dependency through Gunicorn.
- Environment-variable support for OPENAI_API_KEY, OPENAI_MODEL, and PORT.

## 3. Decision Log
| Decision | Reason |
|---|---|
| Keep Flask minimal | Meets the assignment without unnecessary framework complexity. |
| Reuse existing extractor and validator | Avoids duplicating business logic and keeps the web layer thin. |
| Use temporary files | Prevents uploaded invoices from being permanently stored by the application. |
| Use a browser-side table | Makes extracted values and validation errors easy to review. |
| Use Gunicorn for deployment | Provides a production WSGI server instead of Flask's development server. |
| Use Render Blueprint configuration | Gives a repeatable free-tier deployment setup through render.yaml. |
| Read PORT from the environment | Allows the same application to work locally and on hosted platforms. |
| Keep API credentials in environment variables | Prevents secrets from being committed to Git. |

## 4. Sample Usage
1. Start the application locally.
2. Open http://127.0.0.1:5000.
3. Select a PDF invoice.
4. Click Extract Invoice.
5. Review the extracted fields in the table.
6. Review any validation errors shown below the table.

For command-line API testing:
curl.exe -X POST -F "file=@samples\london_invoice.pdf" http://127.0.0.1:5000/extract

## 5. Local Setup
Create and activate a virtual environment, install requirements, create a .env file, and provide:
OPENAI_API_KEY=your_key_here

Optional:
OPENAI_MODEL=gpt-4o-mini

Run:
py app.py

For production-style local testing:
gunicorn app:app

## 6. Render Deployment
1. Push the repository to GitHub.
2. In Render, create a new Blueprint/Web Service from the repository.
3. Render can use render.yaml for the build and start configuration.
4. Add OPENAI_API_KEY as a secret environment variable.
5. Deploy the service.
6. Open the generated Render URL and upload a sample PDF.

Do not commit the actual OpenAI API key to GitHub.

## 7. Verification Status
Application code, extraction/validation integration, UI result table, Docker configuration, and Render configuration are implemented.

Docker runtime verification was not completed because Docker Desktop was unable to start on the development machine. This is an environment/runtime limitation rather than a missing Dockerfile.

## 8. Limitations
- The application depends on a valid OpenAI API key and available API credits.
- Extraction quality depends on the PDF text and configured model.
- The current upload flow accepts PDF files but does not implement user authentication.
- Uploaded files are temporary and are not intended as a permanent document store.
- No database or persistent invoice history is included.
- Docker image execution still needs verification on a working Docker runtime.
- Render free-tier behavior may vary with provider limits and service availability.

## 9. Next-Step Recommendations
1. Verify the Docker image on a machine where Docker Desktop starts correctly.
2. Deploy to Render and test with all sample invoices.
3. Add automated web-route tests using Flask's test client.
4. Add upload-size limits and stronger PDF/content validation.
5. Add authentication if the application will handle private invoices.
6. Add structured application logging and monitoring.
7. Consider persistent storage only if invoice history is required.
8. Add CI to run pytest automatically on every push.

## 10. Sign-Off
Implementation status: Ready for submission, with Docker runtime verification pending.

Known blocker: Docker Desktop startup/runtime issue on the development machine.

Recommended follow-up: Verify Docker locally or in CI, then complete a hosted Render smoke test.
