# Success Metrics

This document establishes the measurable criteria to determine the success of the HospitalityAI platform.

---

## 1. Business Metrics

These metrics verify that the platform delivers operational and guest value:

- **AI Query Deflection Rate**: Percentage of incoming guest queries handled fully by the AI Concierge.
  - *Target*: $\ge 60\%$ of incoming guest messages.
- **Reservation Booking Conversion Rate**: Percentage of conversational booking starts that complete successfully.
  - *Target*: $\ge 15\%$ conversion rate.
- **Room Turnaround Efficiency**: Mean elapsed time from reservation checkout to room status changing to "Clean".
  - *Target*: Decreased by $\ge 20\%$ compared to manual methods.
- **Sentiment Shift**: Indexing positive vs negative guest review ratings.
  - *Target*: Overall average review sentiment score $\ge 4.2 / 5.0$.

---

## 2. Technical Metrics

These metrics verify system stability, latency, and model accuracy:

- **Conversational AI Latency**: Time elapsed from guest message submit to response delivery.
  - *Target*: Mean latency $\le 2.0\text{ seconds}$ (95th percentile $\le 3.5\text{ seconds}$).
- **Occupancy Forecast Error**: The mean absolute percentage error (MAPE) of the 30-day demand forecast model.
  - *Target*: $\text{MAPE} \le 8\%$.
- **Cancellation Classification Accuracy**: Precision and recall of the reservation cancellation model.
  - *Target*: $\text{F1-Score} \ge 0.85$.
- **System Uptime**: Cumulative availability of API endpoints and platforms.
  - *Target*: $\ge 99.9\%$ uptime.

---

## 3. Process & Quality Metrics

These metrics verify codebase quality and engineering health:

- **Test Coverage**: Percentage of code statements covered by automated test runs.
  - *Target*: $\ge 90\%$ test coverage.
- **Static Analysis Compliance**: Linting (Ruff) and typing (Mypy) checks.
  - *Target*: 100% compliance on build steps (zero errors or warnings).
- **Documentation Completeness**: Percentage of public modules, classes, and methods with API docstrings.
  - *Target*: 100% documentation coverage.
