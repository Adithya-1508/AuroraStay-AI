# ETL Specification: Ingestion & Extraction

Defines data extraction specifications and extractors interface rules.

## Extractors Types

1. **CSVExtractor**:
   - Parses flat CSV files (e.g. historical reservation lists).
   - Input: Path to CSV, character encoding (default UTF-8), delimiter (default `,`).
   - Output: List of dictionaries (raw row hashes).
2. **JSONExtractor**:
   - Ingests structured JSON data dumps (e.g. profile preferences, configuration states).
   - Input: Path to JSON.
   - Output: Parsed JSON arrays/dictionaries.
3. **APIExtractor**:
   - Extracts from REST API endpoints (e.g. live guest check-in states from local PMS).
   - Input: URL target, headers context, payload params.
   - Output: JSON payloads.
4. **PMSMockExtractor**:
   - Simulated PMS daily booking extracts.
   - Output: List of reservation data structures.

## Ingestion Registry Rules

- All extractions must capture standard metadata attributes:
  - Source path/URL.
  - Extraction Timestamp.
  - Raw record count.
