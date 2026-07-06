# ETL Specification: Data Loading

Defines loading behaviors, database operations, and data target writes.

## Ingestion Targets

1. **PostgreSQL Target**:
   - Write clean, verified data records directly into the corresponding tables using SQLAlchemy bulk inserts/upserts.
   - Operations:
     - **Upsert**: Match records by unique keys (e.g. `email` for Guests, `id` or composite attributes for Reservations). If matching rows exist, update the contents and bump the `version` field. Otherwise, write new records.
     - **Bulk insert**: For batch runs (e.g. seeding), load rows efficiently in sized chunks (default 1000 rows per transaction chunk).
2. **Metadata target logging**:
   - Upon successful database load, log the pipeline execution stats into the `etl_executions` metadata table:
     - `id`: Unique execution UUID.
     - `dataset_name`: Name of target dataset.
     - `dataset_version`: Version signature (e.g. commit hash or source filename timestamp).
     - `source`: File path or REST URL source reference.
     - `row_counts`: Total rows loaded.
     - `validation_status`: Pipeline run status ("PASSED" / "FAILED").
     - `execution_duration_sec`: Log execution speed in seconds.
