# Data Platform: ETL Pipeline Ingestion

This document details the Extract-Transform-Load (ETL) architecture and operations flow.

## ETL Stages

```
[Extractors] (CSV, JSON, PMS Dumps)
     │
     ▼
[Transformers] (Whitespace Strip, E.164 Phones, Date Casts)
     │
     ▼
[Validator] (Null Checks, Unique Checks, Date Check-in < Check-out)
     │
     ├─── If Invalid ───► [Validation Reports] (Logged as JSON)
     │
     └─── If Valid ────► [Database Loader] ──► [PostgreSQL Target]
                              │
                              ▼
                       [Metadata Catalog] (Log executions metadata)
```

## Module Specifications

1. **Extractors (`backend/etl/extract/`)**:
   - `CSVExtractor`: Uses python standard `csv.DictReader`.
   - `JSONExtractor`: Parses structured JSON configurations.
   - `APIExtractor`: Performs requests fetch routines.
   - `PMSMockExtractor`: Yields realistic hotel reservation data.
2. **Transformers (`backend/etl/transform/`)**:
   - Cleans string characters, lowercase emails, normalizes phone numbers to digits format, and parses dates.
3. **Validator (`backend/etl/validation/`)**:
   - Evaluates integrity rules (cost check, score ranges).
4. **Loaders (`backend/etl/load/`)**:
   - Commits records within database transactions.
