import pytest

from backend.ai.cache.semantic import AICache
from backend.ai.models.registry import ModelRegistry
from backend.ai.prompts.registry import PromptRegistry
from backend.ai.providers.mock import MockProvider
from backend.ai.providers.registry import ProviderRegistry
from backend.ai.routing.router import ModelRouter
from backend.ai.service import AIService
from backend.ai.telemetry.tracker import AITelemetryTracker


@pytest.mark.asyncio
async def test_ai_service_integration() -> None:
    """Verifies end-to-end AIService execution flow."""
    providers = ProviderRegistry()
    models = ModelRegistry()
    router = ModelRouter(models)
    prompts = PromptRegistry()
    cache = AICache()
    telemetry = AITelemetryTracker()

    service = AIService(providers, models, router, prompts, cache, telemetry)

    # Retrieve and configure mock provider responses
    mock_prov: MockProvider = providers.get("mock")  # type: ignore
    mock_prov.add_response(content="Integrated output content")

    messages = [{"role": "user", "content": "planning tasks"}]
    res = await service.generate(
        messages, force_model="mock-model", prompt_version="1.0.0"
    )

    assert res.content == "Integrated output content"
    assert telemetry.get_metrics()["total_calls"] == 1
    assert cache.get(messages, "mock-model", "mock") is not None
