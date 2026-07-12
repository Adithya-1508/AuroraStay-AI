from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from observability.ai_evaluation.model import ModelEvaluator
from observability.ai_evaluation.prompt import PromptEvaluator
from observability.ai_evaluation.rag import RAGEvaluator
from observability.cost.intelligence import CostIntelligence
from observability.drift.detector import DriftDetector
from observability.governance.privacy import PIIRedactor
from observability.governance.registry import GovernanceRegistry
from observability.incidents.service import IncidentService, IncidentSeverity

router = APIRouter(prefix="/observability")


# Request Schemas
class EvaluateRequest(BaseModel):
    evaluation_type: str  # RAG | MODEL | PROMPT
    predictions: list[Any]
    actuals: list[Any]


class AlertTriggerRequest(BaseModel):
    component: str
    severity: str  # INFO | WARNING | CRITICAL
    message: str


# Instances
incident_service = IncidentService()
gov_registry = GovernanceRegistry()


@router.get("/agents", tags=["Observability"])
async def get_monitored_agents() -> list[dict[str, Any]]:
    """Retrieves execution metrics for registered agents."""
    return [
        {
            "agent_name": "GuestConcierge",
            "planning_time_ms": 320.0,
            "execution_time_ms": 1150.0,
            "tool_usage": {"SearchHotelKnowledgeTool": 3},
            "decision_confidence": 0.94,
        },
        {
            "agent_name": "RevenueAgent",
            "planning_time_ms": 480.0,
            "execution_time_ms": 1820.0,
            "tool_usage": {"RetrievePricingPolicy": 1},
            "decision_confidence": 0.89,
        },
    ]


@router.get("/prompts", tags=["Observability"])
async def get_prompt_audit_logs() -> list[dict[str, Any]]:
    """Retrieves prompt variables, versions, and execution success rates."""
    # Simulating logged executions
    raw_prompt = "Hello, first name is John Doe, email is john.doe@email.com, phone is 555-123-4567."
    redacted = PIIRedactor.redact_text(raw_prompt)

    return [
        {
            "name": "concierge_faq",
            "version": "2.1.0",
            "variables_redacted": redacted,
            "success": True,
            "cost": 0.00015,
        }
    ]


@router.get("/models", tags=["Observability"])
async def get_governance_models() -> list[dict[str, Any]]:
    """Lists approved machine learning models and owners."""
    return gov_registry.models


@router.get("/workflows", tags=["Observability"])
async def get_workflow_telemetry() -> list[dict[str, Any]]:
    """Retrieves LangGraph node latency and checkpoint states."""
    return [
        {
            "workflow_name": "RevenueDecisionWorkflow",
            "status": "COMPLETED",
            "duration_ms": 2300,
            "checkpoint_recovered": False,
        }
    ]


@router.get("/incidents", tags=["Observability"])
async def get_incident_tickets(status: str | None = None) -> list[dict[str, Any]]:
    """Retrieves incident tickets logged across services."""
    # Seed a default resolved incident if list is empty
    if not incident_service.list_incidents():
        inc = incident_service.create_incident(
            title="SLA Breach on Sunday evening checkout peak",
            severity=IncidentSeverity.CRITICAL,
            source="WORKFLOW",
            root_cause="Housekeeper staff utilization gap",
        )
        incident_service.resolve_incident(
            incident_id=inc.incident_id,
            resolution="Dynamic re-allocation of 2 staff cleaners",
            lessons_learned="Reschedule housekeeper shift hours",
        )

    return [inc.model_dump() for inc in incident_service.list_incidents(status)]


@router.get("/cost", tags=["Observability"])
async def get_cost_report() -> dict[str, Any]:
    """Retrieves monthly token usage, inference and department USD cost report."""
    mock_runs = [
        {
            "model": "gpt-4",
            "prompt_tokens": 1000,
            "completion_tokens": 500,
            "module": "Revenue",
        },
        {
            "model": "claude-3-opus",
            "prompt_tokens": 800,
            "completion_tokens": 400,
            "module": "GuestConcierge",
        },
        {
            "model": "mock-model",
            "prompt_tokens": 2000,
            "completion_tokens": 1000,
            "module": "DashboardBFF",
        },
    ]
    return CostIntelligence.aggregate_monthly_report(mock_runs)


@router.get("/drift", tags=["Observability"])
async def get_drift_report() -> dict[str, Any]:
    """Computes features, embeddings, and target predictions drift report."""
    detector = DriftDetector()
    return detector.evaluate_system_drift(
        historical_features=[0.70, 0.72, 0.71],
        current_features=[0.75, 0.78, 0.77],
        historical_predictions=[12000.00, 12500.00],
        current_predictions=[14000.00, 14200.00],
    )


@router.get("/evaluation", tags=["Observability"])
async def list_model_evaluations() -> list[dict[str, Any]]:
    """Lists historical model, prompt, and RAG validation metrics."""
    return [
        {
            "target": "forecaster-regressor-v1",
            "metrics": {
                "mean_squared_error": 0.045,
                "r2_score": 0.88,
            },
            "evaluated_at": "2026-07-12T12:00:00Z",
        }
    ]


@router.post("/evaluate", tags=["Observability"])
async def run_observability_evaluation(req: EvaluateRequest) -> dict[str, Any]:
    """Triggers manual evaluation scoring on a dataset."""
    etype = req.evaluation_type.upper()

    if etype == "RAG":
        # Calculate Groundedness on the first pair for verification
        groundedness = RAGEvaluator.evaluate_groundedness(
            output_text=str(req.predictions[0]),
            context_text=str(req.actuals[0]),
        )
        return {
            "evaluation_type": etype,
            "metrics": {
                "groundedness": groundedness,
            },
        }

    elif etype == "MODEL":
        # Calculate MSE/R2 on float metrics
        preds = [float(p) for p in req.predictions]
        acts = [float(a) for a in req.actuals]
        mse = ModelEvaluator.calculate_mse(preds, acts)
        r2 = ModelEvaluator.calculate_r2(preds, acts)

        return {
            "evaluation_type": etype,
            "metrics": {
                "mean_squared_error": mse,
                "r2_score": r2,
            },
        }

    elif etype == "PROMPT":
        # Calculate conformity metrics
        conformity = PromptEvaluator.evaluate_output_conformity(
            output_text=str(req.predictions[0]),
        )
        return {
            "evaluation_type": etype,
            "metrics": {
                "conformity_score": conformity,
            },
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported evaluation type: {req.evaluation_type}",
        )


@router.post("/alerts", tags=["Observability"])
async def trigger_observability_alert(req: AlertTriggerRequest) -> dict[str, Any]:
    """Registers manual operational incidents for SLA or provider alerts."""
    severity_map = {
        "INFO": IncidentSeverity.LOW,
        "WARNING": IncidentSeverity.MEDIUM,
        "CRITICAL": IncidentSeverity.CRITICAL,
    }
    severity = severity_map.get(req.severity.upper(), IncidentSeverity.MEDIUM)

    inc = incident_service.create_incident(
        title=f"Manual Alert: {req.component}",
        severity=severity,
        source=req.component.upper(),
        root_cause=req.message,
    )
    return {
        "alert_registered": True,
        "incident_id": inc.incident_id,
        "details": inc.model_dump(),
    }
