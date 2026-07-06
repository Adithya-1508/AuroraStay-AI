import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from backend.ai.providers.base import BaseProvider, ProviderResponse
from backend.core.settings import settings


class NVIDIAProvider(BaseProvider):
    """NVIDIA NIM provider adapter routing completions via OpenAI endpoints."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or settings.NVIDIA_API_KEY
        self.base_url = base_url or "https://integrate.api.nvidia.com/v1"

    async def generate(
        self,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Sends a completion request to NVIDIA NIM API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
            **kwargs,
        }
        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            choice = data["choices"][0]
            message = choice["message"]
            content = message.get("content") or ""

            tool_calls = []
            if "tool_calls" in message:
                for tc in message["tool_calls"]:
                    tool_calls.append(
                        {
                            "id": tc.get("id"),
                            "name": tc["function"].get("name"),
                            "arguments": json.loads(
                                tc["function"].get("arguments", "{}")
                            )
                            if isinstance(tc["function"].get("arguments"), str)
                            else tc["function"].get("arguments", {}),
                        }
                    )

            usage = data.get("usage") or {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
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
        """Streams a completion request chunk sequence from NVIDIA NIM API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            **kwargs,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            choice = chunk["choices"][0]
                            delta = choice.get("delta", {})
                            content = delta.get("content") or ""
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


__all__ = ["NVIDIAProvider"]
