# Spec: Machine Learning Services

- **Status**: Ready
- **Owner**: Machine Learning Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the business objectives, inputs, outputs, and evaluation metrics for the four core machine learning capabilities: Occupancy Forecasting, Cancellation Classification, Upgrade Recommendations, and Review Sentiment Analysis.

## 2. Responsibilities
- Provide a daily occupancy prediction percentage for the next 30 days.
- Classify active reservations with a cancellation probability score (0.0 to 1.0) and associated risk categories.
- Score and recommend available room upgrades based on guest demographics and reservation parameters.
- Analyze review texts to extract sentiment categories (Positive, Neutral, Negative) and score values.

## 3. Dependencies
- **Data Platform**: To extract training feature tables and historical logs.
- **MLflow Registry**: For model tracking, parameters validation, and model package storage.

## 4. Interfaces
```python
# Conceptual interfaces for Machine Learning Service

class MachineLearningService:
    async def forecast_occupancy(
        self, target_date: date
    ) -> OccupancyForecastSchema:
        """Returns the forecasted occupancy rate and confidence bounds for a target date."""
        pass

    async def predict_cancellation_risk(
        self, reservation_id: str
    ) -> CancellationRiskSchema:
        """Returns the probability and risk indicators of a booking cancellation."""
        pass

    async def recommend_upgrades(
        self, reservation_id: str
    ) -> List[UpgradeRecommendationSchema]:
        """Rank and return eligible room type upgrades for a reservation."""
        pass

    async def analyze_sentiment(self, text: str) -> SentimentResultSchema:
        """Evaluates review text for polarity and sentiment category."""
        pass
```

## 5. Configuration
- `ML_MODEL_VERSION`: The tag indicating current active model variant in registry.
- `CANCELLATION_RISK_THRESHOLDS`: Dict defining boundaries (e.g. $\ge 0.70$ is High Risk).

## 6. Error Handling
- `ModelNotReadyError`: Raised if inference is called before a model is loaded or trained.
- `FeatureExtractionError`: Raised when query input is missing feature columns needed by model.

## 7. Security
- Restrict training pipelines so they do not process raw personally identifiable information (PII).
- Sanitize review texts to prevent input injections in sentiment evaluation.

## 8. Testing
- **Model Accuracy Verification**:
  - Test pipeline checks target metrics: Occupancy Forecast MAPE $\le 8\%$, Cancellation F1-Score $\ge 0.85$.
- **Latency Verification**:
  - Ensure individual inference runs take $\le 100\text{ ms}$.

## 9. Acceptance Criteria
- [ ] Forecast updates daily and exposes model confidence bounds.
- [ ] Cancellation risk probability is calculated immediately on reservation creation.
- [ ] Sentiment analyzer correctly flags negative reviews containing urgent guest complaints.
