import re


def parse_invoice(text: str) -> dict:
    """
    Extract structured information from a WanderWays travel invoice.
    """

    # Invoice number
    invoice_number = None

    match = re.search(
        r"Invoice\s*(?:No\.?|Number|#)\s*[:\-]?\s*([A-Z0-9\-]+)",
        text,
        re.IGNORECASE
    )

    if match:
        invoice_number = match.group(1)

    # Travel date
    travel_date = None

    match = re.search(
        r"Travel\s*Date\s*[:\-]?\s*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        text,
        re.IGNORECASE
    )

    if match:
        travel_date = match.group(1)

    # Return date
    return_date = None

    match = re.search(
        r"Return\s*Date\s*[:\-]?\s*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        text,
        re.IGNORECASE
    )

    if match:
        return_date = match.group(1)

    # Currency
    currency = None

    match = re.search(
        r"\b(USD|GBP|EUR|CAD|AUD|AED|SAR|PKR)\b|[$£€]",
        text,
        re.IGNORECASE
    )

    if match:
        currency = match.group(1) if match.group(1) else match.group(0)

    # Final TOTAL - specifically look for TOTAL, not Subtotal
    total_amount = None

    match = re.search(
        r"\bTOTAL\b\s*[:\-]?\s*[$£€]?\s*([0-9,]+(?:\.[0-9]{2})?)",
        text,
        re.IGNORECASE
    )

    if match:
        total_amount = match.group(1).replace(",", "")

    # Payment status
    payment_status = None

    match = re.search(
        r"Payment\s*Status\s*:\s*([A-Za-z]+)",
        text,
        re.IGNORECASE
    )

    if match:
        payment_status = match.group(1)

    # Payment method
    payment_method = None

    match = re.search(
        r"Payment\s*Method\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        payment_method = match.group(1).strip()

    return {
        "invoice_number": invoice_number,
        "travel_date": travel_date,
        "return_date": return_date,
        "currency": currency,
        "total_amount": total_amount,
        "payment_status": payment_status,
        "payment_method": payment_method
    }