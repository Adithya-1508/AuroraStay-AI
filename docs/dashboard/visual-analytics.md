# Visual Analytics Manual

## Overview
AI Visual Analytics converts numerical lists and charts into readable text descriptions with primary causes, actions, and projected business impacts.

## API
- **POST** `/api/v1/dashboard/visual-analytics/explain`
  - **Body**:
    ```json
    {
      "chart_type": "LINE_CHART",
      "metric_name": "Revenue",
      "historical_data": [100, 105],
      "forecast_data": [110, 115]
    }
    ```
  - **Output**: JSON payload with parsed `status`, bulleted list of `causes`, `actions`, and projected `expected_impact` value.
