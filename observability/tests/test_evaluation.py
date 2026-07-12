import pytest

from observability.ai_evaluation.model import ModelEvaluator
from observability.ai_evaluation.prompt import PromptEvaluator
from observability.ai_evaluation.rag import RAGEvaluator
from observability.cost.intelligence import CostIntelligence
from observability.drift.detector import DriftDetector


def test_rag_evaluation_metrics() -> None:
    # 1. Groundedness check
    output = "Deluxe room is clean. Spa price is $50."
    context = "Deluxe room is clean. Spa price is $50. Check out is at 11am."
    score = RAGEvaluator.evaluate_groundedness(output, context)
    assert score == 1.0

    output_partial = "Deluxe room is clean. Spa price is $999."  # 999 not in context
    score_partial = RAGEvaluator.evaluate_groundedness(output_partial, context)
    assert score_partial < 1.0

    # Empty output case
    assert RAGEvaluator.evaluate_groundedness("", context) == 1.0

    # 2. Precision & Recall check
    ret = ["chunk-1", "chunk-2"]
    gt = ["chunk-2", "chunk-3"]
    metrics = RAGEvaluator.evaluate_retrieval(ret, gt)
    assert metrics["precision"] == 0.5
    assert metrics["recall"] == 0.5

    # Empty sets
    assert RAGEvaluator.evaluate_retrieval([], []) == {"precision": 1.0, "recall": 1.0}

    # 3. Citations check
    text_cite = "Policy states check-out time is 11am [Check-out Rules](file:///docs/checkout.md)"
    urls = ["file:///docs/checkout.md"]
    assert RAGEvaluator.evaluate_citations(text_cite, urls) == 1.0
    assert RAGEvaluator.evaluate_citations("No citations", urls) == 1.0


def test_model_evaluation_metrics() -> None:
    # 1. MSE
    preds = [1.1, 2.0, 3.2]
    acts = [1.0, 2.0, 3.0]
    mse = ModelEvaluator.calculate_mse(preds, acts)
    assert mse == pytest.approx(0.0167, abs=1e-3)
    assert ModelEvaluator.calculate_mse([], [1.0]) == 0.0

    # 2. R2
    r2 = ModelEvaluator.calculate_r2(preds, acts)
    assert r2 > 0.9
    assert ModelEvaluator.calculate_r2([1.0], [1.0]) == 1.0
    assert ModelEvaluator.calculate_r2([1.0, 1.0], [1.0, 1.0]) == 1.0

    # 3. Classification
    preds_cls = [1, 0, 1, 0]
    acts_cls = [1, 1, 0, 0]
    cls_metrics = ModelEvaluator.calculate_classification_metrics(preds_cls, acts_cls)
    assert cls_metrics["precision"] == 0.5
    assert cls_metrics["recall"] == 0.5
    assert cls_metrics["f1_score"] == 0.5

    # No predictions
    assert ModelEvaluator.calculate_classification_metrics([], []) == {
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0,
    }

    # 4. Demographic Parity
    group_rates = {"Bronze": 0.8, "Gold": 1.0}
    parity = ModelEvaluator.calculate_demographic_parity(group_rates)
    assert parity == 0.8
    assert ModelEvaluator.calculate_demographic_parity({}) == 1.0
    assert ModelEvaluator.calculate_demographic_parity({"Group": 0.0}) == 1.0


def test_prompt_evaluation_metrics() -> None:
    # 1. Output conformity
    out_valid_json = '{"occupancy": 0.8, "adr": 150}'
    score_valid = PromptEvaluator.evaluate_output_conformity(
        out_valid_json, ["occupancy", "adr"]
    )
    assert score_valid == 1.0

    score_invalid = PromptEvaluator.evaluate_output_conformity(
        out_valid_json, ["invalid_key"]
    )
    assert score_invalid == 0.0

    # Short length check
    assert PromptEvaluator.evaluate_output_conformity("abc", min_length=5) == 0.5
    # Invalid JSON
    assert PromptEvaluator.evaluate_output_conformity("not-json", ["key"]) == 0.1

    # 2. Success rate
    logs = [{"success": True}, {"success": False}, {"success": True}]
    assert PromptEvaluator.calculate_prompt_success_rate(logs) == pytest.approx(
        0.667, rel=1e-3
    )
    assert PromptEvaluator.calculate_prompt_success_rate([]) == 1.0


def test_drift_detector() -> None:
    detector = DriftDetector()

    # Empty features check
    assert detector.calculate_psi([], []) == 0.0
    # Zero division check
    assert detector.calculate_psi([0.0], [1.0]) == 0.0

    # Trigger drift alerts
    res = detector.evaluate_system_drift(
        historical_features=[1.0, 1.0],
        current_features=[2.0, 2.0],  # PSI = 1.0 > 0.25 (triggers feat_drift CRITICAL)
        historical_predictions=[1.0, 1.0],
        current_predictions=[
            2.0,
            2.0,
        ],  # PSI = 1.0 > 0.25 (triggers pred_drift WARNING)
    )
    assert res["drift_detected"] is True
    assert len(res["alerts_raised"]) == 2


def test_cost_intelligence_recommendations() -> None:
    # Low cost report recommendations empty check
    low_runs = [
        {"model": "gpt-3.5-turbo", "prompt_tokens": 100, "completion_tokens": 50}
    ]
    res = CostIntelligence.aggregate_monthly_report(low_runs)
    assert len(res["recommendations"]) == 0
