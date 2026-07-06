from collections.abc import Callable
from typing import Any


class AIEvaluator:
    """Evaluator validating response outputs against golden expectations."""

    def evaluate_response(self, content: str, expected_keywords: list[str]) -> float:
        """Scores keyword presence ratio inside response content."""
        if not expected_keywords:
            return 1.0
        found = sum(1 for kw in expected_keywords if kw.lower() in content.lower())
        return found / len(expected_keywords)

    def run_benchmark(
        self,
        golden_dataset: list[dict[str, Any]],
        generate_fn: Callable[[list[dict[str, Any]]], str],
    ) -> dict[str, Any]:
        """Runs evaluation iterations checking accuracy rates across cases list."""
        results = []
        total_score = 0.0

        for case in golden_dataset:
            messages = case["messages"]
            expected = case.get("expected_keywords") or []

            try:
                output = generate_fn(messages)
                score = self.evaluate_response(output, expected)
                passed = score >= case.get("min_score", 0.5)
            except Exception as e:
                output = f"ERROR: {e}"
                score = 0.0
                passed = False

            results.append(
                {
                    "messages": messages,
                    "output": output,
                    "score": score,
                    "passed": passed,
                }
            )
            total_score += score

        avg_score = total_score / len(golden_dataset) if golden_dataset else 1.0
        return {
            "average_score": round(avg_score, 4),
            "cases_run": len(golden_dataset),
            "results": results,
        }


__all__ = ["AIEvaluator"]
