# Spec: Revenue Domain Aggregate

- **Status**: Ready
- **Owner**: Revenue Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the pricing rules, rates multipliers, and demand forecast aggregates.

## 2. Responsibilities
- Model occupancy forecasting timelines.
- Calculate booking cancellation risks.
- Aggregate nightly revenues.

## 3. Public Interfaces
```python
class RevenueForecast:
    def __init__(self, forecast_id: str, date_range: DateRange):
        self.forecast_id = forecast_id
        self.date_range = date_range
        self.predictions = {}  # Map date -> Occupancy percentage

    def set_prediction(self, target_date: date, value: float) -> None:
        if not (0.0 <= value <= 1.0):
            raise ValueError("Occupancy value must be between 0.0 and 1.0.")
        self.predictions[target_date] = value
```

## 4. Invariants
- Forecast calculations cannot span date ranges greater than 30 nights.
