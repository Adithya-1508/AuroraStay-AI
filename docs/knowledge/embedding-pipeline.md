# Embedding Pipeline Manual

The `EmbeddingPipeline` coordinates batch vector generation using the AI Platform backend.

## Features

- **Batch Execution**: Bundles chunk lists to save API call round-trips.
- **Content Hashing Caching**: Computes SHA256 hashes of texts, retrieving existing vectors from local dictionary caches to bypass model fees.
- **Versioning**: Signatures embedding models to check index integrity.
