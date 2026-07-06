from typing import Any


class KnowledgeVersioningManager:
    """Manages document, embedding, chunking, and vector index version alignments."""

    def __init__(self) -> None:
        self._registry: dict[str, dict[str, Any]] = {}

    def register_version(
        self,
        document_id: str,
        doc_version: str,
        embedding_version: str,
        chunk_version: str,
        index_version: str,
    ) -> None:
        """Registers a set of configurations mapped to a document ID."""
        self._registry[document_id] = {
            "document_id": document_id,
            "document_version": doc_version,
            "embedding_version": embedding_version,
            "chunk_version": chunk_version,
            "index_version": index_version,
        }

    def get_document_version(self, document_id: str) -> dict[str, Any] | None:
        """Retrieves configuration parameters mapped to document ID."""
        return self._registry.get(document_id)

    def verify_versions(
        self,
        document_id: str,
        doc_version: str,
        embedding_version: str,
        chunk_version: str,
    ) -> bool:
        """Validates if target signatures match registered version states."""
        record = self.get_document_version(document_id)
        if not record:
            return False
        return (
            record["document_version"] == doc_version
            and record["embedding_version"] == embedding_version
            and record["chunk_version"] == chunk_version
        )


__all__ = ["KnowledgeVersioningManager"]
