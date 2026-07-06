# RAG Specification: Embedding Pipeline

This document describes the batch embedding generation and caching layer.

## Embedding Generation Abstraction

Integrates directly with AI Platform models configurations:
- **Batch Processing**: Groups chunks into batches (e.g. size 16 or 32) before submitting requests to optimize speed.
- **Embedding Cache**: Caches embedding vectors by content hash in an in-memory or Redis key-value store to skip redundant generations.
- **Embedding Versioning**: Tracks the specific embedding model name and version used (e.g. `nomic-embed-text-v1.5`) to prevent mismatches on reload.
