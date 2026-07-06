from typing import Any

from ..embeddings.client import EmbeddingPipeline
from ..indexing.qdrant import QdrantIndexer


class Retriever:
    """Semantic retrieval engine querying vectors from database indices."""

    def __init__(
        self, indexer: QdrantIndexer, embedding_pipeline: EmbeddingPipeline
    ) -> None:
        self.indexer = indexer
        self.embedding_pipeline = embedding_pipeline
        self._query_expansion_hooks: list[Any] = []

    def register_query_expansion_hook(self, hook: Any) -> None:
        """Registers a hook function for dynamically rewriting queries."""
        self._query_expansion_hooks.append(hook)

    async def retrieve(
        self,
        query: str,
        collection_name: str = "hotel-knowledge",
        filter_meta: dict[str, Any] | None = None,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """Processes query, maps vector similarity search, and normalizes scores."""
        expanded_query = query
        for hook in self._query_expansion_hooks:
            expanded_query = await hook(expanded_query)

        query_vector = await self.embedding_pipeline.get_embedding(expanded_query)

        hits = await self.indexer.search(
            collection_name=collection_name,
            query_vector=query_vector,
            filter_meta=filter_meta,
            top_k=top_k,
        )

        results = []
        for hit in hits:
            score = hit["score"]
            normalized_score = (
                (score + 1.0) / 2.0
                if -1.0 <= score <= 1.0
                else max(0.0, min(1.0, score))
            )
            results.append(
                {
                    "chunk_id": hit["id"],
                    "content": hit["payload"].get("content", ""),
                    "score": normalized_score,
                    "metadata": {
                        k: v for k, v in hit["payload"].items() if k != "content"
                    },
                }
            )

        return results


__all__ = ["Retriever"]
