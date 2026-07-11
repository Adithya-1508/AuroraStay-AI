# Reports Engine Manual

## Overview
The Reports Engine compiles Daily, Weekly, Monthly, or Quarterly performance files. It aggregates KPIs across reservations, operations, guests, and revenue, and calls the RAG platform to retrieve context policies for generating executive summaries.

## APIs
- **GET** `/api/v1/dashboard/reports`: Fetch previous generated reports metadata.
- **POST** `/api/v1/dashboard/reports/generate`: Run the LLM over metrics to compile insights.
  - **Body**:
    ```json
    {
      "interval": "WEEKLY",
      "department": "ALL",
      "custom_notes": "Focus on spa drop"
    }
    ```
  - **Output**: Returns an `AIReportPackage` containing structured KPIs, summary paragraphs, list of insights, and list of recommended actions.
