from backend.ai.models.registry import ModelRegistry
from backend.ai.routing.router import ModelRouter


def test_model_router_task_selection() -> None:
    """Verifies router model selection for planning and summarization."""
    registry = ModelRegistry()
    router = ModelRouter(registry)

    # Summarization should prefer Ollama
    model_sum = router.select_model(task="summarization")
    assert model_sum.provider == "ollama"

    # Planning should prefer NVIDIA
    model_plan = router.select_model(task="planning")
    assert model_plan.provider == "nvidia"


def test_model_router_fallback_chain() -> None:
    """Verifies that the router determines correct fallback providers."""
    registry = ModelRegistry()
    router = ModelRouter(registry)

    assert router.get_fallback_provider("nvidia") == "ollama"
    assert router.get_fallback_provider("ollama") == "mock"
    assert router.get_fallback_provider("mock") is None
