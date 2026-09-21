# System Architecture

## Invoice Extraction Workflow

The WanderWays Invoice Extractor follows a simple document processing workflow:

```text
Travel Invoice PDF
        ↓
PDF Reader
        ↓
Text Extraction
        ↓
Invoice Data Processing
        ↓
Structured Invoice Data
        ↓
Output / Storage