import pytest

from backend.ai.providers.mock import MockProvider


@pytest.mark.asyncio
async def test_mock_provider_generation() -> None:
    """Verifies that the mock provider returns predefined responses correctly."""
    provider = MockProvider()
    provider.add_response(
        content="Success content",
        tool_calls=[{"id": "call_1", "name": "get_guest", "arguments": {}}],
        usage={"prompt_tokens": 15, "completion_tokens": 10, "total_tokens": 25},
    )

    response = await provider.generate(
        messages=[{"role": "user", "content": "hello"}], model="mock-model"
    )

    assert response.content == "Success content"
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0]["name"] == "get_guest"
    assert response.usage["total_tokens"] == 25
    assert response.model_name == "mock-model"


@pytest.mark.asyncio
async def test_mock_provider_streaming() -> None:
    """Verifies that the mock provider yields streaming response chunks."""
    provider = MockProvider()
    provider.add_response(content="Streaming chunk")

    chunks = []
    async for chunk in provider.generate_stream(
        messages=[{"role": "user", "content": "hello"}], model="mock-model"
    ):
        chunks.append(chunk)

    assert len(chunks) == 1
    assert chunks[0].content == "Streaming chunk"
