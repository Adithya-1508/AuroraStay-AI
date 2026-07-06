from abc import ABC, abstractmethod


class BaseEmbeddingService(ABC):
    """Abstract base class standardizing embeddings generation actions."""

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Generates embedding vector for a single text input string."""
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generates embedding vectors for a batch of text input strings."""
        pass


class MockEmbeddingService(BaseEmbeddingService):
    """Mock Embedding Service returning deterministic vectors for local testing."""

    def __init__(self, dimension: int = 1536) -> None:
        self.dimension = dimension
        self._cache: dict[str, list[float]] = {}

    async def embed_text(self, text: str) -> list[float]:
        """Generates a mock vector based on string hash characteristics."""
        if text in self._cache:
            return self._cache[text]

        # Deterministic generation using basic character variations
        val = len(text) / 1000.0
        vec = [val] * self.dimension
        self._cache[text] = vec
        return vec

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generates batch vectors sequentially."""
        return [await self.embed_text(t) for t in texts]


__all__ = ["BaseEmbeddingService", "MockEmbeddingService"]
