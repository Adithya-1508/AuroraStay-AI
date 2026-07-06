from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any


@dataclass
class ProviderResponse:
    """Normalized response schema returned by any AI Platform provider."""

    content: str
    tool_calls: list[dict[str, Any]]
    usage: dict[str, int]
    model_name: str


class BaseProvider(ABC):
    """Abstract base class defining standardized LLM connection boundaries."""

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Sends inference call to LLM, returning a normalized response."""
        pass

    @abstractmethod
    def generate_stream(
        self,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> AsyncIterator[ProviderResponse]:
        """Sends inference call to LLM, yielding normalized streaming chunks."""
        pass


__all__ = ["ProviderResponse", "BaseProvider"]
