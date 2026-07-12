# Model Evaluation Manual

## Overview
Model Evaluation measures accuracy indicators and fairness compliance across all deployed ML classifiers and forecasting regressors.

## Indicators
- **Mean Squared Error (MSE)**: The mean squared difference between predictions and actual values.
- **R2 Score**: Coefficient of determination measuring model variance fit.
- **Classification Metrics**: Precision, Recall, and F1 score for binary classifiers.
- **Demographic Parity**: Ratio of acceptance rates between bronze, silver, and gold guest segments to check for bias.

## APIs
- **GET** `/api/v1/observability/evaluation`: Fetch evaluation history.
- **POST** `/api/v1/observability/evaluate` (evaluation_type: MODEL): Triggers MSE and R2 validations on predictions.
