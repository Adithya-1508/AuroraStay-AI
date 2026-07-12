from typing import Any


class CostIntelligence:
    """Calculates USD values from token metrics and outputs optimization plans."""

    # Simulated prices in USD per 1,000 tokens
    TOKEN_PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.0020},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "mock-model": {"input": 0.001, "output": 0.002},
    }

    @classmethod
    def calculate_call_cost(
        cls, model: str, prompt_tokens: int, completion_tokens: int
    ) -> float:
        """Calculates total cost in USD for a single LLM invocation."""
        pricing = cls.TOKEN_PRICING.get(model, {"input": 0.0015, "output": 0.0020})
        cost_in = (prompt_tokens / 1000) * pricing["input"]
        cost_out = (completion_tokens / 1000) * pricing["output"]
        return float(cost_in + cost_out)

    @classmethod
    def aggregate_monthly_report(cls, runs: list[dict[str, Any]]) -> dict[str, Any]:
        """Synthesizes total cost and generates cache optimization advice."""
        total_usd = 0.0
        by_module: dict[str, float] = {}

        for run in runs:
            model = run.get("model", "mock-model")
            p_tokens = run.get("prompt_tokens", 0)
            c_tokens = run.get("completion_tokens", 0)
            module = run.get("module", "General")

            cost = cls.calculate_call_cost(model, p_tokens, c_tokens)
            total_usd += cost
            by_module[module] = by_module.get(module, 0.0) + cost

        recommendations = []
        if total_usd > 10.0:
            recommendations.append(
                "Inference query volumes are high. Recommend enabling AICache TTL of 4 hours to reduce token costs."
            )

        return {
            "total_cost": total_usd,
            "currency": "USD",
            "breakdown": {"by_module": by_module},
            "recommendations": recommendations,
        }
