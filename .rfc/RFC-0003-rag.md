# RFC-0003: Knowledge Platform & RAG Ingestion Design

- **Author**: Antigravity AI Coding Agent
- **Status**: Draft
- **Date**: 2026-07-04
- **Target Release/Loop**: Loop 09

## 1. Summary
This RFC proposes the design of the RAG ingestion pipeline, document chunking parameters, and vector indexing configurations.

## 2. Proposed Design

### Document Ingestion Flow
We propose an automated ingestion flow triggered when documents are uploaded to MinIO buckets:
```
MinIO Bucket Upload ──► Parser ──► Recursive Chunker ──► Vector Indexing (Qdrant)
```

### Chunking Parameters
- **Strategy**: Recursive Character Text Chunker.
- **Chunk Size**: `256` tokens.
- **Overlap**: `32` tokens.
- This ensures we retain structural context while keeping chunks small enough to prevent retrieval noise.

### Vector Retrieval & Reranking
- Embed query inputs using the default embedding provider.
- Query the `hotel_faqs` collection in Qdrant, retrieving the top 5 chunks.
- Apply a similarity threshold check (default: `0.75`).
- (Optional) Use a reranker model (e.g. Cohere rerank or local equivalent) to select the top 3 chunks, building the final context block for the LLM prompt.

## 3. Testing and Verification
- Run semantic retrieval tests on sample questions (e.g. pool hours, room checkout policies), verifying that returned chunks contain the correct answers.
