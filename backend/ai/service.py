import time
from typing import Any

from backend.ai.cache.semantic import AICache
from backend.ai.models.registry import ModelRegistry
from backend.ai.prompts.registry import PromptRegistry
from backend.ai.providers.base import BaseProvider, ProviderResponse
from backend.ai.providers.registry import ProviderRegistry
from backend.ai.routing.router import ModelRouter
from backend.ai.telemetry.tracker import AITelemetryTracker


class AIService:
    """Core AI Service orchestrating prompts, router, caching, and adapters."""

    def __init__(
        self,
        providers: ProviderRegistry,
        models: ModelRegistry,
        router: ModelRouter,
        prompts: PromptRegistry,
        cache: AICache,
        telemetry: AITelemetryTracker,
    ) -> None:
        self.providers = providers
        self.models = models
        self.router = router
        self.prompts = prompts
        self.cache = cache
        self.telemetry = telemetry

    async def generate(
        self,
        messages: list[dict[str, Any]],
        task: str | None = None,
        requires_tools: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        tools: list[dict[str, Any]] | None = None,
        force_model: str | None = None,
        prompt_version: str | None = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Executes LLM request, performing cache lookups and provider failovers."""
        # 1. Resolve target model configuration
        if force_model:
            model_meta = self.models.get(force_model)
        else:
            model_meta = self.router.select_model(task, requires_tools)

        # 2. Check cache hits
        cached = self.cache.get(messages, model_meta.name, model_meta.provider)
        if cached:
            assert isinstance(cached, ProviderResponse)
            return cached

        # 3. Inference call execution with provider failover logic
        provider_name = model_meta.provider
        model_name = model_meta.name
        start_time = time.time()
        retry_count = 0
        success = False
        failure_reason = None
        response = None

        while True:
            try:
                provider: BaseProvider = self.providers.get(provider_name)
                response = await provider.generate(
                    messages=messages,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    tools=tools,
                    **kwargs,
                )
                success = True
                break
            except Exception as e:
                fallback = self.router.get_fallback_provider(provider_name)
                if fallback:
                    provider_name = fallback
                    # Map fallback model names
                    if fallback == "ollama":
                        model_name = "llama3"
                    else:
                        model_name = "mock-model"
                    retry_count += 1
                else:
                    failure_reason = str(e)
                    break

        latency = time.time() - start_time

        # 4. Log inference metrics in Telemetry Tracker
        self.telemetry.log_inference(
            model=model_name,
            provider=provider_name,
            latency_sec=latency,
            prompt_tokens=response.usage["prompt_tokens"] if response else 0,
            completion_tokens=response.usage["completion_tokens"] if response else 0,
            total_tokens=response.usage["total_tokens"] if response else 0,
            success=success,
            prompt_version=prompt_version,
            failure_reason=failure_reason,
            retry_count=retry_count,
        )

        if not success:
            raise RuntimeError(f"AI Platform generate call failed: {failure_reason}")

        assert response is not None
        # 5. Populate cache
        self.cache.set(messages, model_meta.name, model_meta.provider, response)
        return response


__all__ = ["AIService"]
