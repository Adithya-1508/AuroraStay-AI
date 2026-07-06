import time
from dataclasses import dataclass
from typing import Any


@dataclass
class InferenceTrace:
    """Trace logs representing a single LLM request."""

    model: str
    provider: str
    prompt_version: str | None
    latency_sec: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    success: bool
    failure_reason: str | None
    retry_count: int
    timestamp: float


class AITelemetryTracker:
    """Tracker accumulating trace statistics and latencies summaries."""

    def __init__(self) -> None:
        self.traces: list[InferenceTrace] = []

    def log_inference(
        self,
        model: str,
        provider: str,
        latency_sec: float,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        success: bool,
        prompt_version: str | None = None,
        failure_reason: str | None = None,
        retry_count: int = 0,
    ) -> None:
        """Appends a new inference request run report trace."""
        self.traces.append(
            InferenceTrace(
                model=model,
                provider=provider,
                prompt_version=prompt_version,
                latency_sec=latency_sec,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                success=success,
                failure_reason=failure_reason,
                retry_count=retry_count,
                timestamp=time.time(),
            )
        )

    def get_metrics(self) -> dict[str, Any]:
        """Compiles aggregate latency, token cost, and success rate indicators."""
        total = len(self.traces)
        if total == 0:
            return {
                "total_calls": 0,
                "success_rate": 1.0,
                "avg_latency": 0.0,
                "total_tokens": 0,
            }

        successes = sum(1 for t in self.traces if t.success)
        total_tokens = sum(t.total_tokens for t in self.traces)
        avg_latency = sum(t.latency_sec for t in self.traces) / total

        return {
            "total_calls": total,
            "success_rate": successes / total,
            "avg_latency": round(avg_latency, 4),
            "total_tokens": total_tokens,
        }

    def clear(self) -> None:
        """Clears all logged telemetry traces."""
        self.traces.clear()


__all__ = ["InferenceTrace", "AITelemetryTracker"]
