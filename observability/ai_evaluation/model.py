class ModelEvaluator:
    """Computes forecasting accuracy, classification metrics, and fairness indicators."""

    @staticmethod
    def calculate_mse(predictions: list[float], actuals: list[float]) -> float:
        """Computes Mean Squared Error (MSE)."""
        if not predictions or len(predictions) != len(actuals):
            return 0.0
        n = len(predictions)
        squared_errors = [(predictions[i] - actuals[i]) ** 2 for i in range(n)]
        return float(sum(squared_errors) / n)

    @staticmethod
    def calculate_r2(predictions: list[float], actuals: list[float]) -> float:
        """Computes Coefficient of Determination (R2 Score)."""
        if not predictions or len(predictions) != len(actuals) or len(actuals) < 2:
            return 1.0
        n = len(predictions)
        mean_actual = sum(actuals) / n
        ss_res = sum((actuals[i] - predictions[i]) ** 2 for i in range(n))
        ss_tot = sum((actuals[i] - mean_actual) ** 2 for i in range(n))
        if ss_tot == 0:
            return 1.0
        return float(1.0 - (ss_res / ss_tot))

    @staticmethod
    def calculate_classification_metrics(
        predictions: list[int], actuals: list[int]
    ) -> dict[str, float]:
        """Computes Precision, Recall, and F1 score."""
        tp = fp = fn = tn = 0
        for p, a in zip(predictions, actuals, strict=False):
            if p == 1 and a == 1:
                tp += 1
            elif p == 1 and a == 0:
                fp += 1
            elif p == 0 and a == 1:
                fn += 1
            else:
                tn += 1

        precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = (
            float(2 * precision * recall / (precision + recall))
            if (precision + recall) > 0
            else 0.0
        )

        return {"precision": precision, "recall": recall, "f1_score": f1}

    @staticmethod
    def calculate_demographic_parity(
        selection_rates_by_group: dict[str, float],
    ) -> float:
        """Computes the demographic parity ratio to assess fairness."""
        # Standard metric is ratio of lowest selection rate to highest selection rate
        if not selection_rates_by_group:
            return 1.0
        rates = list(selection_rates_by_group.values())
        min_rate = min(rates)
        max_rate = max(rates)
        if max_rate == 0:
            return 1.0
        return float(min_rate / max_rate)
