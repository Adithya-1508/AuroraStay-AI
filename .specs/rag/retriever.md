# RAG Specification: Retriever

This document details semantic retrievals and filters in Qdrant.

## Vector Index Specifications

- **Qdrant Collection**: Maps documents to active collections (e.g. `hotel-knowledge`).
- **Namespaces & Filters**: Supports filtering by document metadata fields (e.g. `department = 'housekeeping'`, `version = '2.0'`) using Qdrant payload filters.

## Retrieval Process

1. Embeds query string.
2. Calls Qdrant vector search using cosine similarity distance metric.
3. Standardizes result scores to a normalized range: $[0.0, 1.0]$.
4. Returns top-k matching chunks.
