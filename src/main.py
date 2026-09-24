import json
import logging
import sys

from .invoice_extractor import extract_invoice_data

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: py -m src.main <invoice.pdf>")
    print(json.dumps(extract_invoice_data(sys.argv[1]), indent=2))

if __name__ == "__main__":
    main()
