import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowTrace:
    """Represents a logged execution trace of an agent workflow."""

    thread_id: str
    goal: str
    duration_sec: float
    tool_latencies: dict[str, float] = field(default_factory=dict)
    retry_counts: dict[str, int] = field(default_factory=dict)
    success: bool = True
    failure_reason: str | None = None
    execution_path: list[str] = field(default_factory=list)
    token_usage: dict[str, int] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class AgentTelemetryTracker:
    """Telemetry tracker aggregating workflow executions statistics."""

    def __init__(self) -> None:
        self.traces: list[WorkflowTrace] = []

    def log_workflow(self, trace: WorkflowTrace) -> None:
        """Saves an execution trace snapshot."""
        self.traces.append(trace)

    def get_metrics(self) -> dict[str, Any]:
        """Compiles average duration and success rate summaries."""
        total = len(self.traces)
        if total == 0:
            return {
                "total_workflows": 0,
                "success_rate": 1.0,
                "avg_duration": 0.0,
            }

        successes = sum(1 for t in self.traces if t.success)
        avg_dur = sum(t.duration_sec for t in self.traces) / total

        return {
            "total_workflows": total,
            "success_rate": successes / total,
            "avg_duration": round(avg_dur, 4),
        }

    def clear(self) -> None:
        """Resets trace records cache."""
        self.traces.clear()


__all__ = ["WorkflowTrace", "AgentTelemetryTracker"]
