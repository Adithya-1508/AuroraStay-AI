import os
from typing import Any

import structlog

logger = structlog.get_logger()

try:
    import mlflow

    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False


class MLflowTracker:
    """Wrapper class surrounding MLflow client commands with offline fallbacks."""

    def __init__(self, tracking_uri: str | None = None) -> None:
        self.tracking_uri: str = (
            tracking_uri
            or os.getenv("MLFLOW_TRACKING_URI")
            or "sqlite:///mlflow.db"
        )
        self.active_run: Any = None

        if MLFLOW_AVAILABLE:
            try:
                mlflow.set_tracking_uri(self.tracking_uri)
            except Exception as e:
                logger.warning(
                    "Failed to configure MLflow tracking URI",
                    uri=self.tracking_uri,
                    error=str(e),
                )

    def start_run(self, experiment_name: str, run_name: str | None = None) -> Any:
        """Starts a tracking run context."""
        if MLFLOW_AVAILABLE:
            try:
                mlflow.set_experiment(experiment_name)
                self.active_run = mlflow.start_run(run_name=run_name)
                return self.active_run
            except Exception as e:
                logger.warning(
                    "Failed to start MLflow run, falling back to local mock run",
                    error=str(e),
                )
                self.active_run = "mock_run"
        else:
            self.active_run = "mock_run"
        return self.active_run

    def end_run(self) -> None:
        """Ends the active tracking run."""
        if MLFLOW_AVAILABLE and self.active_run and self.active_run != "mock_run":
            try:
                mlflow.end_run()
            except Exception as e:
                logger.warning("Failed to end MLflow run", error=str(e))
        self.active_run = None

    def log_param(self, key: str, value: Any) -> None:
        """Logs a training parameter."""
        logger.info("ML Parameter logged", key=key, value=value)
        if MLFLOW_AVAILABLE and self.active_run and self.active_run != "mock_run":
            try:
                mlflow.log_param(key, value)
            except Exception as e:
                logger.warning("Failed to log MLflow parameter", key=key, error=str(e))

    def log_metric(self, key: str, value: float) -> None:
        """Logs a validation metric."""
        logger.info("ML Metric logged", key=key, value=value)
        if MLFLOW_AVAILABLE and self.active_run and self.active_run != "mock_run":
            try:
                mlflow.log_metric(key, value)
            except Exception as e:
                logger.warning("Failed to log MLflow metric", key=key, error=str(e))

    def log_model(self, model: Any, artifact_path: str) -> None:
        """Logs model artifacts (scikit-learn models, etc.)."""
        logger.info("ML Model artifact logged", artifact_path=artifact_path)
        if MLFLOW_AVAILABLE and self.active_run and self.active_run != "mock_run":
            try:
                # Log using generic python model saving or scikit-learn flavor
                mlflow.sklearn.log_model(model, artifact_path)
            except Exception as e:
                logger.warning(
                    "Failed to log MLflow model artifact",
                    path=artifact_path,
                    error=str(e),
                )
