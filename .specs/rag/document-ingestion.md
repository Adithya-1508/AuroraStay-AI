# RAG Specification: Document Ingestion

This document details the document ingestion pipeline.

## Ingestion Flow

```
[Document File (PDF, etc)]
           │
           ▼
     [File Parser] ──► Extracted Text & Structure
           │
           ▼
     [Chunk Engine] ──► Chunks Array with Metadata
           │
           ▼
  [Embedding Pipeline] ──► Chunks + Vector Embeddings
           │
           ▼
    [Vector Index] ──► Indexed into Qdrant collections
```

## Supported Parsers

- **PDFParser**: Uses pdfminer or similar to extract text and locations.
- **DOCXParser**: Extracts text and paragraph hierarchies.
- **MarkdownParser**: Extracts headings and section boundaries.
- **HTMLParser**: Strips markup and parses layout.
- **CSV/JSONParser**: Parses tabular and dictionary keys.
