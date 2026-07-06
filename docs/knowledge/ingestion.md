# Document Ingestion Manual

The `KnowledgeIngestionService` orchestrates parsing, metadata extraction, chunking, and vector database uploads.

## Component Reference

- `ParserFactory`: Resolves document file extensions to their corresponding parsers (Markdown, HTML, PDF, Word, CSV, JSON).
- `KnowledgeIngestionService.ingest(file_path)`: Runs the ingestion pipeline and registers version configurations.
