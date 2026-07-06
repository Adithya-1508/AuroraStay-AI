from collections.abc import AsyncIterator
from typing import Any

from backend.ai.providers.base import BaseProvider, ProviderResponse


class MockProvider(BaseProvider):
    """Mock Provider returning deterministic outputs to bypass remote API calls."""

    def __init__(self) -> None:
        self.responses: list[ProviderResponse] = []
        self.default_content = "Mock response content"
        self.default_tool_calls: list[dict[str, Any]] = []

    def add_response(
        self,
        content: str,
        tool_calls: list[dict[str, Any]] | None = None,
        usage: dict[str, int] | None = None,
    ) -> None:
        """Adds a predefined response to be returned sequentially by generator."""
        self.responses.append(
            ProviderResponse(
                content=content,
                tool_calls=tool_calls or [],
                usage=usage
                or {
                    "prompt_tokens": 10,
                    "completion_tokens": 10,
                    "total_tokens": 20,
                },
                model_name="mock-model",
            )
        )

    async def generate(
        self,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Simulates response extraction."""
        if self.responses:
            return self.responses.pop(0)
        return ProviderResponse(
            content=self.default_content,
            tool_calls=self.default_tool_calls,
            usage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
            model_name=model,
        )

    async def generate_stream(
        self,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> AsyncIterator[ProviderResponse]:
        """Yields mock response chunk."""
        response = await self.generate(
            messages, model, temperature, max_tokens, **kwargs
        )
        yield response


__all__ = ["MockProvider"]
