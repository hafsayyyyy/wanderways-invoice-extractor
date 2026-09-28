from src.validator import validate_invoice


def test_valid_invoice():
    invoice = {
        "invoice_number": "WW-001",
        "travel_date": "2026-09-20",
        "return_date": "2026-09-27",
        "vendor_name": "WanderWays Travel",
        "total_amount": 2178.00
    }

    is_valid, errors = validate_invoice(invoice)

    assert is_valid is True
    assert errors == []


def test_invalid_invoice():
    invoice = {
        "invoice_number": "WW-002",
        "travel_date": "2026-09-20",
        "return_date": "2026-09-27",
        "vendor_name": "",
        "total_amount": 2178.00
    }

    is_valid, errors = validate_invoice(invoice)

    assert is_valid is False
    assert len(errors) > 0