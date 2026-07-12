from typing import Any


class PromptEvaluator:
    """Evaluates prompt configurations, execution success rates, and template drift."""

    @staticmethod
    def evaluate_output_conformity(
        output_text: str,
        expected_json_keys: list[str] | None = None,
        min_length: int = 5,
    ) -> float:
        """Scores prompt outputs based on validation rules (length, key presence)."""
        score = 1.0

        # Rule 1: Length check
        if len(output_text) < min_length:
            score -= 0.5

        # Rule 2: JSON key validation
        if expected_json_keys:
            import json

            try:
                data = json.loads(output_text)
                keys_found = sum(1 for k in expected_json_keys if k in data)
                score *= float(keys_found / len(expected_json_keys))
            except json.JSONDecodeError:
                score *= 0.1  # severe penalty if not valid JSON

        return max(0.0, score)

    @staticmethod
    def calculate_prompt_success_rate(logs: list[dict[str, Any]]) -> float:
        """Calculates success rates from a list of execution logs."""
        if not logs:
            return 1.0
        successes = sum(1 for log in logs if log.get("success", False))
        return float(successes / len(logs))
