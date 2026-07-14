class RiskEvaluator:
    """Evaluates security telemetry logs to score threat risk levels."""

    @staticmethod
    def calculate_request_risk(
        failed_logins: int,
        prompt_injection_flags: int,
        unauthorized_attempts: int,
    ) -> float:
        """Computes a normalized risk score from 0.0 (safe) to 1.0 (critical threat)."""
        score = 0.0

        # Login failure contributions
        score += min(failed_logins * 0.15, 0.30)

        # Prompt injection contributes immediately to critical risk
        if prompt_injection_flags > 0:
            score += 0.70

        # Privilege/Authorization failure contributions
        score += min(unauthorized_attempts * 0.10, 0.20)

        return min(score, 1.0)

    @classmethod
    def get_risk_label(cls, score: float) -> str:
        """Resolves score value to risk rating label."""
        if score >= 0.70:
            return "CRITICAL"
        elif score >= 0.40:
            return "HIGH"
        elif score >= 0.15:
            return "MEDIUM"
        return "LOW"
