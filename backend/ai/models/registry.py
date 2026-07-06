from dataclasses import dataclass


@dataclass
class ModelMetadata:
    """Metadata tracking features, window parameters, and costs for a model."""

    name: str
    provider: str
    context_window: int
    max_tokens: int
    input_cost_per_1k: float
    output_cost_per_1k: float
    supports_streaming: bool
    supports_tools: bool


class ModelRegistry:
    """Registry maintaining active maps of available model configurations."""

    def __init__(self) -> None:
        self._models: dict[str, ModelMetadata] = {}
        # Prepopulate default target models configuration
        self.register(
            ModelMetadata(
                name="meta/llama3-70b-instruct",
                provider="nvidia",
                context_window=8192,
                max_tokens=2048,
                input_cost_per_1k=0.0007,
                output_cost_per_1k=0.0009,
                supports_streaming=True,
                supports_tools=True,
            )
        )
        self.register(
            ModelMetadata(
                name="llama3",
                provider="ollama",
                context_window=8192,
                max_tokens=2048,
                input_cost_per_1k=0.0,
                output_cost_per_1k=0.0,
                supports_streaming=True,
                supports_tools=True,
            )
        )
        self.register(
            ModelMetadata(
                name="mock-model",
                provider="mock",
                context_window=4096,
                max_tokens=1024,
                input_cost_per_1k=0.0,
                output_cost_per_1k=0.0,
                supports_streaming=True,
                supports_tools=True,
            )
        )

    def register(self, metadata: ModelMetadata) -> None:
        """Saves a model metadata specification record."""
        self._models[metadata.name.strip().lower()] = metadata

    def get(self, name: str) -> ModelMetadata:
        """Retrieves a model metadata record by name. Raises ValueError if not found."""
        meta = self._models.get(name.strip().lower())
        if not meta:
            raise ValueError(f"Model '{name}' is not registered.")
        return meta

    def list_models(self) -> list[ModelMetadata]:
        """Lists all registered models."""
        return list(self._models.values())


__all__ = ["ModelMetadata", "ModelRegistry"]
