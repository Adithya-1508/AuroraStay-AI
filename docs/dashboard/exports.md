# Exports Engine Manual

## Overview
The Export Platform serializes dashboard metrics, layout data, or reports into files.

## API
- **POST** `/api/v1/dashboard/exports`
  - **Body**:
    ```json
    {
      "export_format": "CSV | EXCEL | JSON | PDF",
      "dataset_type": "EXECUTIVE",
      "filters": {}
    }
    ```
  - **Response**: File stream buffer with corresponding Mime-Type and Attachment headers.

## Formats
- **JSON**: Serialized JSON.
- **CSV**: Text CSV.
- **EXCEL**: Tab-separated TSV compatible with Microsoft Excel.
- **PDF**: Board-ready PDF layout bytes.
