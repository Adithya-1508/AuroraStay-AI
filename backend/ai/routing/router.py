from backend.ai.models.registry import ModelMetadata, ModelRegistry
from backend.core.settings import settings


class ModelRouter:
    """Intelligent router selecting models and resolving failover paths."""

    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry
        self.fallback_chain = ["nvidia", "ollama", "mock"]

    def select_model(
        self, task: str | None = None, requires_tools: bool = False
    ) -> ModelMetadata:
        """Selects a model metadata configuration matching task requirements."""
        models = self.registry.list_models()

        # 1. Routing based on target tasks
        if task == "planning":
            for m in models:
                if m.provider == "nvidia" and m.supports_tools:
                    return m
        elif task == "summarization":
            for m in models:
                if m.provider == "ollama":
                    return m

        # 2. Routing based on tools requirements
        if requires_tools:
            for m in models:
                if m.supports_tools:
                    return m

        # 3. Fallback to default configured parameters
        try:
            return self.registry.get(settings.DEFAULT_MODEL)
        except ValueError:
            return self.registry.get("mock-model")

    def get_fallback_provider(self, current_provider: str) -> str | None:
        """Determines the next provider in the fallback chain to mitigate timeouts."""
        prov = current_provider.strip().lower()
        if prov not in self.fallback_chain:
            return None
        idx = self.fallback_chain.index(prov)
        if idx + 1 < len(self.fallback_chain):
            return self.fallback_chain[idx + 1]
        return None


__all__ = ["ModelRouter"]
