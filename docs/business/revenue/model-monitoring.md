# Model Registry & Drift Monitoring

The platform maintains model quality using structured pipelines and registry tools.

## Model Registry
All models (e.g., `OccupancyRegressor`, `GuestClusterer`) are registered in the `ModelRegistry` catalog:
- **Promotion**: Promotes model versions to `Production` status.
- **Rollback**: Rolls back to the previously active `Production` version if anomalies are discovered.

## Training Pipeline
- Automated K-Means fitting for segmentation.
- Offline regressor training for forecasting.

## Drift Monitoring
The `MonitoringPipeline` compares inference baseline distributions against current features:
- **Calculation**: Computes a Kolmogorov-Smirnov (KS) statistic or drift score over target variables.
- **Alerting**: Dispatches event logs when scores exceed predefined thresholds.
