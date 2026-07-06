import pytest
from pydantic import BaseModel

from backend.ai.providers.mock import MockProvider
from backend.ai.structured_output.parser import StructuredOutputParser


class GuestSummary(BaseModel):
    name: str
    vip: bool


def test_structured_output_parsing() -> None:
    """Verifies that the parser parses json and validates it against Pydantic models."""
    parser = StructuredOutputParser()

    # Valid JSON with code block
    json_text = '```json\n{\n  "name": "Sarah",\n  "vip": true\n}\n```'
    res = parser.parse(json_text, GuestSummary)
    assert res.name == "Sarah"
    assert res.vip is True


@pytest.mark.asyncio
async def test_structured_output_retry_success() -> None:
    """Verifies that the parser corrects malformed outputs via retry loops."""
    provider = MockProvider()
    # Attempt 0: Malformed JSON
    provider.add_response(content="Malformed text here")
    # Attempt 1: Correct JSON
    provider.add_response(content='{"name": "Elena", "vip": false}')

    parser = StructuredOutputParser(provider)
    res = await parser.parse_with_retry(
        messages=[{"role": "user", "content": "summarize"}],
        model=GuestSummary,
        model_name="mock-model",
    )

    assert res.name == "Elena"
    assert res.vip is False
