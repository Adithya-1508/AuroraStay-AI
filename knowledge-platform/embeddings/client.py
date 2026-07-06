import hashlib

from backend.ai.embeddings.service import (
    BaseEmbeddingService,
    MockEmbeddingService,
)


class EmbeddingPipeline:
    """Batch embedding generator client carrying content hashing cache controls."""

    def __init__(
        self,
        embedding_service: BaseEmbeddingService | None = None,
        model_version: str = "nomic-embed-v1.5",
    ) -> None:
        self.service = embedding_service or MockEmbeddingService()
        self.model_version = model_version
        self._cache: dict[str, list[float]] = {}

    def _hash_content(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    async def get_embedding(self, text: str) -> list[float]:
        """Fetches vector embedding for text, checking local cache first."""
        h = self._hash_content(text)
        if h in self._cache:
            return self._cache[h]

        vector = await self.service.embed_text(text)
        self._cache[h] = vector
        return vector

    async def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Processes a batch of texts, fetching only uncached entries from model."""
        results = []
        uncached_texts = []
        uncached_indices = []

        for idx, text in enumerate(texts):
            h = self._hash_content(text)
            if h in self._cache:
                results.append((idx, self._cache[h]))
            else:
                uncached_texts.append(text)
                uncached_indices.append(idx)

        if uncached_texts:
            vectors = await self.service.embed_batch(uncached_texts)
            for idx, vec in zip(uncached_indices, vectors, strict=True):
                h = self._hash_content(texts[idx])
                self._cache[h] = vec
                results.append((idx, vec))

        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]


__all__ = ["EmbeddingPipeline"]
