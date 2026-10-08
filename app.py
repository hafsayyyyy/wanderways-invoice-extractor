import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, render_template

from src.invoice_extractor import extract_invoice_data
from src.validator import validate_invoice

app = Flask(__name__)

ALLOWED_EXTENSIONS = {".pdf"}


@app.route("/", methods=["GET"])
def home():
    """Display the invoice upload web page."""
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract_invoice():
    """Upload a PDF invoice, extract its data, and validate the result."""

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No PDF file was uploaded."
        }), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    extension = Path(uploaded_file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({
            "success": False,
            "error": "Only PDF files are allowed."
        }), 400

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            uploaded_file.save(temp_file.name)
            temp_path = temp_file.name

        extracted_data = extract_invoice_data(temp_path)

        required_extraction_fields = [
            "invoice_date",
            "total_amount",
            "vendor_name",
            "travel_dates",
            "booking_reference"
        ]

        extraction_failed = all(
            extracted_data.get(field) in (None, [], "")
            for field in required_extraction_fields
        )

        if extraction_failed:
            return jsonify({
                "success": False,
                "error": (
                    "Invoice extraction failed. "
                    "Please check your OpenAI API key, "
                    "API credits, or model configuration."
                ),
                "data": extracted_data
            }), 500

        is_valid, errors = validate_invoice(extracted_data)

        return jsonify({
            "success": True,
            "valid": is_valid,
            "data": extracted_data,
            "validation_errors": errors
        }), 200

    except Exception:
        app.logger.exception("Invoice processing failed")

        return jsonify({
            "success": False,
            "error": (
                "Invoice processing failed. "
                "Please check the server logs."
            )
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                app.logger.warning(
                    "Could not delete temporary file: %s",
                    temp_path
                )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"

    app.run(
        debug=debug,
        host="0.0.0.0",
        port=port
    )
