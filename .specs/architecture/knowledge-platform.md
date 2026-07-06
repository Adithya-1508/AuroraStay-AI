# Spec: Knowledge Platform & RAG

- **Status**: Ready
- **Owner**: RAG & AI Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define semantic document parsing logic, text chunk partitioning rules, vector embeddings conversions, and Qdrant search index integrations.

## 2. Responsibilities
- Parse text documents (PDFs, TXT files) uploaded to object storage.
- Chunk parsed text using sliding window strategies.
- Request semantic embeddings from cloud vectorizer APIs.
- Upsert points containing text payloads into Qdrant collections.
- Execute similarity searches to retrieve context segments.

## 3. Dependencies
- **Qdrant (Vector DB)**: Storage engine.
- **Embedding Provider API**: Cloud generator (e.g. text-embedding-004).

## 4. Public Interfaces
```python
class VectorStorageAdapter(ABC):
    @abstractmethod
    async def search_similar(
        self, query_vector: List[float], limit: int, threshold: float
    ) -> List[VectorPayloadSchema]:
        """Queries Qdrant and filters based on threshold scores."""
        pass

    @abstractmethod
    async def upsert_points(self, collection: str, points: List[PointStruct]) -> bool:
        """Loads points containing embeddings and metadata into vector index."""
        pass
```

## 5. Configuration
- `VECTOR_DB_URL`: Connection string for Qdrant (e.g. `http://qdrant:6333`).
- `VECTOR_DIMENSION`: Expected dimensions of the embedding (e.g. `1536`).
- `RAG_CHUNK_SIZE`: Token length constraint per chunk (default: `256`).
- `RAG_CHUNK_OVERLAP`: Overlap token margin (default: `32`).

## 6. Failure Modes
- **Vector DB Unreachable**: The retrieval pipeline falls back to database lookup based on keyword matches, logging a WARNING.
- **Embedding Generation Failures**: Retries up to 3 times before raising `EmbeddingServiceUnavailable` error.

## 7. Security Considerations
- Filter points in Qdrant based on session context permissions.
- Validate ingested files to prevent file upload vulnerabilities.

## 8. Testing Strategy
- **Unit Tests**: Mock embeddings calls to verify chunking calculations and overlap logic.
- **Integration Tests**: Execute real semantic inserts and queries against a local Qdrant collection instance.
