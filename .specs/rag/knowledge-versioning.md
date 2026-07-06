# RAG Specification: Knowledge Versioning

This document describes version tracking across document lifecycle layers.

## Version Layers

To enable safe re-indexing, rollbacks, and sync:
- **Document Version**: Tracks updates in document content (e.g. `doc_v1`).
- **Embedding Version**: Model key used to create vectors (e.g. `nomic-embed-v1.5`).
- **Chunk Version**: Split configurations signature (e.g. `chunk_size_500_overlap_50`).
- **Index Version**: Map identifier pointing to current namespace collections.
