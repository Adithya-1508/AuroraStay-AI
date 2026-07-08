import structlog

from business.revenue.ml.registry import ModelRegistration, ModelRegistry
from business.revenue.ml.tracker import MLflowTracker

logger = structlog.get_logger()


class TrainingPipeline:
    """Manages the training, scoring, evaluation, and registration of ML models."""

    def __init__(
        self,
        registry: ModelRegistry | None = None,
        tracker: MLflowTracker | None = None,
    ) -> None:
        self.registry = registry or ModelRegistry()
        self.tracker = tracker or MLflowTracker()

    async def run_forecasting_training(self) -> ModelRegistration:
        """Simulates training of the occupancy forecasting model and registers it."""
        self.tracker.start_run(
            "ForecastingModelExperiment", "train_occupancy_regressor"
        )

        # Log mock parameters & metric scores
        self.tracker.log_param("estimator_type", "LinearRegression")
        self.tracker.log_param(
            "features", ["historical_bookings", "seasonality_index", "day_of_week"]
        )
        self.tracker.log_metric("R2_score", 0.89)
        self.tracker.log_metric("MSE", 0.045)

        # Save registration
        registration = ModelRegistration(
            model_name="OccupancyRegressor",
            version="1.0.0",
            training_dataset="hospital_bookings_2025_v1",
            metrics={"R2_score": 0.89, "MSE": 0.045},
            feature_set=["historical_bookings", "seasonality_index", "day_of_week"],
            owner="Revenue ML Team",
            deployment_status="Production",
            file_path="models/occupancy_regressor.pkl",
        )
        self.registry.register_model(registration)
        self.tracker.end_run()

        logger.info(
            "Forecasting model trained and registered successfully",
            model_id=str(registration.model_id),
        )
        return registration

    async def run_segmentation_training(self) -> ModelRegistration:
        """Simulates training of guest segmentation model and registers it."""
        self.tracker.start_run("SegmentationModelExperiment", "train_guest_clusterer")

        self.tracker.log_param("estimator_type", "KMeans")
        self.tracker.log_param("n_clusters", 4)
        self.tracker.log_metric("inertia", 12.45)

        registration = ModelRegistration(
            model_name="GuestClusterer",
            version="1.0.0",
            training_dataset="guest_profiles_2025_v1",
            metrics={"inertia": 12.45},
            feature_set=["stay_frequency", "total_spending"],
            owner="Revenue ML Team",
            deployment_status="Production",
            file_path="models/guest_clusterer.pkl",
        )
        self.registry.register_model(registration)
        self.tracker.end_run()

        logger.info(
            "Segmentation model trained and registered successfully",
            model_id=str(registration.model_id),
        )
        return registration
