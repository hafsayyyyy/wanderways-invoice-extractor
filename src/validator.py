import json
from datetime import datetime
from jsonschema import Draft7Validator


INVOICE_SCHEMA = {
    "type": "object",
    "required": [
        "invoice_number",
        "travel_date",
        "return_date",
        "vendor_name",
        "total_amount"
    ],
    "properties": {
        "invoice_number": {
            "type": "string"
        },
        "travel_date": {
            "type": "string"
        },
        "return_date": {
            "type": "string"
        },
        "vendor_name": {
            "type": "string"
        },
        "total_amount": {
            "type": "number"
        }
    },
    "additionalProperties": True
}


def validate_invoice(data):
    """
    Validate extracted invoice data.

    Returns:
        tuple: (is_valid, errors)
    """

    errors = []

    # Check that input is a dictionary
    if not isinstance(data, dict):
        return False, ["Invoice data must be a JSON object."]

    # JSON schema validation
    validator = Draft7Validator(INVOICE_SCHEMA)

    for error in validator.iter_errors(data):
        field = ".".join(str(part) for part in error.path)

        if error.validator == "required":
            errors.append(error.message)
        elif field:
            errors.append(f"{field}: {error.message}")
        else:
            errors.append(error.message)

    # Check ISO date format
    for field in ["travel_date", "return_date"]:
        if field in data and isinstance(data[field], str):
            try:
                datetime.strptime(data[field], "%Y-%m-%d")
            except ValueError:
                errors.append(
                    f"{field} must use ISO format YYYY-MM-DD."
                )

    # Check total amount is numeric
    if "total_amount" in data:
        if not isinstance(data["total_amount"], (int, float)):
            errors.append("total_amount must be a numeric value.")

    return len(errors) == 0, errors


def validate_json(json_text):
    """
    Validate a JSON string.

    Returns:
        tuple: (is_valid, errors)
    """

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as error:
        return False, [
            f"Invalid JSON: {error.msg} at line {error.lineno}, column {error.colno}."
        ]

    return validate_invoice(data)