from typing import Any

import structlog

from business.revenue.ml.registry import ModelRegistry
from business.revenue.ml.tracker import MLflowTracker

logger = structlog.get_logger()


class MonitoringPipeline:
    """Monitors model metrics, latencies, feature/label drifts, and issues alerts on degradation."""

    def __init__(
        self,
        registry: ModelRegistry | None = None,
        tracker: MLflowTracker | None = None,
    ) -> None:
        self.registry = registry or ModelRegistry()
        self.tracker = tracker or MLflowTracker()

    async def check_drift(
        self, model_name: str, baseline_values: list[float], current_values: list[float]
    ) -> dict[str, Any]:
        """Calculates prediction drift using differences in mean/deviations."""
        if not baseline_values or not current_values:
            return {"drift_detected": False, "drift_score": 0.0}

        avg_baseline = sum(baseline_values) / len(baseline_values)
        avg_current = sum(current_values) / len(current_values)

        drift_score = abs(avg_baseline - avg_current)
        drift_detected = drift_score > 0.15

        self.tracker.start_run("ModelMonitoringExperiment", f"drift_check_{model_name}")
        self.tracker.log_metric("drift_score", drift_score)
        self.tracker.log_metric("drift_detected", float(drift_detected))
        self.tracker.end_run()

        if drift_detected:
            logger.warning(
                "Prediction drift detected!",
                model_name=model_name,
                drift_score=drift_score,
                threshold=0.15,
            )

        return {
            "drift_detected": drift_detected,
            "drift_score": drift_score,
            "metric_name": "WassersteinDistanceMock",
        }

    async def log_inference_metrics(self, latency_ms: float, has_error: bool) -> None:
        """Records latency and failure metrics."""
        self.tracker.start_run("InferenceMetricsExperiment", "log_inference")
        self.tracker.log_metric("latency_ms", latency_ms)
        self.tracker.log_metric("has_error", float(has_error))
        self.tracker.end_run()
