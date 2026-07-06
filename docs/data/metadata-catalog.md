# Data Platform: Metadata Catalog

This document details the schema of the catalog executions logging.

## Executions Logging

Every ETL injection runs logging parameters in the `etl_executions` table:
- **`dataset_name`**: Logical name of dataset.
- **`dataset_version`**: Version identifier of raw dataset file.
- **`source`**: Path referencing files source location.
- **`timestamp`**: Time of data ingestion.
- **`row_counts`**: Total record counts.
- **`validation_status`**: Output status of validation checks.
- **`execution_duration_sec`**: Ingestion speed metric.
- **`error_report`**: Details on validation errors, if any.
