import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from backend.ai.providers.base import BaseProvider, ProviderResponse
from backend.core.settings import settings


class OllamaProvider(BaseProvider):
    """Ollama local model deployment provider adapter routing requests to api/chat."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or settings.OLLAMA_API_URL

    async def generate(
        self,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Sends a completion request to Ollama API."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
            **kwargs,
        }
        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

            message = data.get("message", {})
            content = message.get("content") or ""

            tool_calls = []
            if "tool_calls" in message:
                for tc in message["tool_calls"]:
                    tool_calls.append(
                        {
                            "id": None,
                            "name": tc["function"].get("name"),
                            "arguments": tc["function"].get("arguments"),
                        }
                    )

            prompt_eval = data.get("prompt_eval_count", 0)
            eval_count = data.get("eval_count", 0)
            usage = {
                "prompt_tokens": prompt_eval,
                "completion_tokens": eval_count,
                "total_tokens": prompt_eval + eval_count,
            }

            return ProviderResponse(
                content=content,
                tool_calls=tool_calls,
                usage=usage,
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
        """Streams a completion request chunk sequence from Ollama API."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
            **kwargs,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST", f"{self.base_url}/api/chat", json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            message = chunk.get("message", {})
                            content = message.get("content") or ""
                            if content:
                                yield ProviderResponse(
                                    content=content,
                                    tool_calls=[],
                                    usage={
                                        "prompt_tokens": 0,
                                        "completion_tokens": 0,
                                        "total_tokens": 0,
                                    },
                                    model_name=model,
                                )
                        except json.JSONDecodeError:
                            pass


__all__ = ["OllamaProvider"]
