# RAG Specification: Chunking

This document describes the chunking strategies and metadata schemas.

## Strategies

1. **Fixed-Size Chunking**: Chunks text by character limits (e.g. 500 characters) with overlap (e.g. 50 characters).
2. **Recursive Character Chunking**: Recursively splits on structural boundaries (paragraphs, sentences, spaces) to fit limits.
3. **Section-Aware Chunking**: Preserves structural units based on document headers and sections.

## Metadata Schema

Every generated chunk must record:
- `document_id`: Unique UUID of source document.
- `chunk_id`: Unique UUID of chunk.
- `section`: Heading path or section name.
- `page`: Page number in original document.
- `content`: Actual text content.
- `version`: Version signature of document.
