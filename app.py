import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request

from src.invoice_extractor import extract_invoice_data
from src.validator import validate_invoice

app = Flask(__name__)

ALLOWED_EXTENSIONS = {".pdf"}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "WanderWays Invoice Extractor",
        "status": "running"
    })


@app.route("/extract", methods=["POST"])
def extract_invoice():
    if "file" not in request.files:
        return jsonify({
            "error": "No PDF file was uploaded."
        }), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({
            "error": "No file selected."
        }), 400

    extension = Path(uploaded_file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({
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

        is_valid, errors = validate_invoice(extracted_data)

        return jsonify({
            "success": True,
            "valid": is_valid,
            "data": extracted_data,
            "validation_errors": errors
        })

    except Exception as exc:
        app.logger.exception("Invoice processing failed")

        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(debug=True)