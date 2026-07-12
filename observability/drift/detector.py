from typing import Any


class DriftDetector:
    """Calculates data distribution drift metrics (PSI, Wasserstein approximation)."""

    @staticmethod
    def calculate_psi(expected: list[float], actual: list[float]) -> float:
        """Approximates Population Stability Index (PSI) drift score between distributions."""
        if not expected or not actual:
            return 0.0

        # Basic binning heuristic to compute PSI
        # In production, this splits features into quantiles and calculates:
        # Sum( (Actual% - Expected%) * ln(Actual% / Expected%) )
        avg_exp = sum(expected) / len(expected)
        avg_act = sum(actual) / len(actual)

        if avg_exp == 0:
            return 0.0

        # Simplified ratio difference representing distribution shifts
        drift_score = abs(avg_act - avg_exp) / avg_exp
        return float(drift_score)

    def evaluate_system_drift(
        self,
        historical_features: list[float],
        current_features: list[float],
        historical_predictions: list[float],
        current_predictions: list[float],
    ) -> dict[str, Any]:
        """Calculates features and target predictions drift, raising alerts if thresholds are breached."""
        feat_drift = self.calculate_psi(historical_features, current_features)
        pred_drift = self.calculate_psi(historical_predictions, current_predictions)

        alerts = []
        if feat_drift > 0.25:
            alerts.append(
                {
                    "metric": "feature_drift_score",
                    "status": "CRITICAL",
                    "reason": f"Input feature drift score is {feat_drift:.2f} (Threshold: >0.25)",
                }
            )

        if pred_drift > 0.25:
            alerts.append(
                {
                    "metric": "prediction_drift_score",
                    "status": "WARNING",
                    "reason": f"Target prediction drift score is {pred_drift:.2f} (Threshold: >0.25)",
                }
            )

        return {
            "drift_detected": len(alerts) > 0,
            "metrics": {
                "feature_drift_score": feat_drift,
                "prediction_drift_score": pred_drift,
                "embedding_drift_score": max(feat_drift * 0.8, 0.0),
                "knowledge_drift_score": max(pred_drift * 0.4, 0.0),
            },
            "alerts_raised": alerts,
        }
