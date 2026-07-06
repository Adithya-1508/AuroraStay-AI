import json
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from backend.ai.providers.base import BaseProvider

T = TypeVar("T", bound=BaseModel)


class StructuredOutputParser:
    """Parser validating raw LLM content against Pydantic schemas."""

    def __init__(self, provider: BaseProvider | None = None) -> None:
        self.provider = provider

    def parse(self, text: str, model: type[T]) -> T:
        """Parses a text payload, returning validated model."""
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        return model.model_validate(data)

    async def parse_with_retry(
        self,
        messages: list[dict[str, Any]],
        model: type[T],
        model_name: str,
        max_retries: int = 2,
    ) -> T:
        """Runs completion, retrying with error feedback if output is invalid."""
        if self.provider is None:
            raise ValueError("Provider is required to perform retries.")

        current_messages = list(messages)
        for attempt in range(max_retries + 1):
            response = await self.provider.generate(current_messages, model_name)
            try:
                return self.parse(response.content, model)
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt == max_retries:
                    raise e

                current_messages.append(
                    {"role": "assistant", "content": response.content}
                )
                current_messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"Your response did not match the validation schema. "
                            f"Error: {e}. Please correct your output and return only "
                            f"valid JSON."
                        ),
                    }
                )

        raise RuntimeError("Retry loop exited unexpectedly.")


__all__ = ["StructuredOutputParser"]
