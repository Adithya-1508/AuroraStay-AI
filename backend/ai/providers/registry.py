from backend.ai.providers.base import BaseProvider
from backend.ai.providers.mock import MockProvider
from backend.ai.providers.nvidia import NVIDIAProvider
from backend.ai.providers.ollama import OllamaProvider


class ProviderRegistry:
    """Registry maintaining active maps of LLM connection provider instances."""

    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}
        # Pre-register default standard providers
        self.register("nvidia", NVIDIAProvider())
        self.register("ollama", OllamaProvider())
        self.register("mock", MockProvider())

    def register(self, name: str, provider: BaseProvider) -> None:
        """Saves a provider instance under a key name."""
        self._providers[name.strip().lower()] = provider

    def get(self, name: str) -> BaseProvider:
        """Retrieves a provider instance by name. Raises ValueError if not found."""
        prov = self._providers.get(name.strip().lower())
        if not prov:
            raise ValueError(f"Provider '{name}' is not registered.")
        return prov


__all__ = ["ProviderRegistry"]
