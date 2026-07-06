# RFC-0004: ML Platform and Forecasting Pipelines Design

- **Author**: Antigravity AI Coding Agent
- **Status**: Draft
- **Date**: 2026-07-04
- **Target Release/Loop**: Loop 13 — Loop 14

## 1. Summary
This RFC proposes the ML training and inference pipeline designs for occupancy forecasting and cancellation classification.

## 2. Proposed Design

### Occupancy Forecasting (Prophet/XGBoost)
- **Feature Engineering**: Extract daily occupancy history, calendar seasons, local events, and weekend indicators.
- **Model**: We propose a hybrid model (Prophet for seasonality, XGBoost for residual features) trained on historical room reservation data.
- **Output**: Daily occupancy forecasting percentage for the next 30 days.

### Cancellation Classification (Random Forest/LightGBM)
- **Features**: Lead time, booking channel, average daily rate, deposit type, and special requests count.
- **Inference**: Triggered when a new booking is created. Returns a cancellation risk probability (0.0 to 1.0) and associated risk tags.

### Model Tracking & Promotion (MLflow)
- Log metrics (MAPE, MSE, F1-scores) and model parameters to MLflow.
- Models that pass our validation thresholds (MAPE $\le 8\%$, F1-score $\ge 0.85$) are registered in the MLflow Model Registry and promoted to `Production`.

```
Train Run ──► Log parameters (MLflow) ──► Validation Check ──► Promote to Production
```

## 3. Testing and Verification
- Run model validation scripts against historical test sets, verifying accuracy targets before model promotion.
