import uuid
from datetime import datetime
from typing import Any, TypedDict

import structlog
from knowledge_platform.retrieval.engine import Retriever
from langgraph.graph import END, START, StateGraph

from business.revenue.domain.value_objects import DecisionPackage
from business.revenue.forecasting.service import ForecastingService
from business.revenue.pricing.engine import PricingEngine

logger = structlog.get_logger()


class AgentState(TypedDict):
    room_category_id: uuid.UUID
    target_date: datetime
    occupancy_ratio: float
    is_peak_season: bool
    policy_docs: str
    decision_package: dict[str, Any]
    explanation: str


class RevenueAgent:
    """LangGraph-orchestrated Decision Intelligence Agent generating explainable dynamic pricing strategies."""

    def __init__(
        self,
        forecasting_service: ForecastingService,
        pricing_engine: PricingEngine,
        retriever: Retriever | None = None,
    ) -> None:
        self.forecasting_service = forecasting_service
        self.pricing_engine = pricing_engine
        self.retriever = retriever

        # Build Graph DAG
        builder = StateGraph(AgentState)

        # Nodes
        builder.add_node("policy_retriever", self.retrieve_policy_node)
        builder.add_node("decision_builder", self.build_decision_node)
        builder.add_node("decision_explainer", self.explain_decision_node)

        # Transitions
        builder.add_edge(START, "policy_retriever")
        builder.add_edge("policy_retriever", "decision_builder")
        builder.add_edge("decision_builder", "decision_explainer")
        builder.add_edge("decision_explainer", END)

        self.graph = builder.compile()

    async def retrieve_policy_node(self, state: AgentState) -> dict[str, Any]:
        """Queries the Knowledge Platform for pricing policy caps and constraints."""
        policy_text = "Standard pricing policy limits markups to 30%."
        if self.retriever:
            try:
                # Query RAG collection for pricing limits
                res = await self.retriever.retrieve("dynamic pricing limits markup cap")
                if res:
                    policy_text = "\n".join([doc.content for doc in res])
            except Exception as e:
                logger.warning(
                    "RAG policy retrieval failed, using fallback limits", error=str(e)
                )

        return {"policy_docs": policy_text}

    async def build_decision_node(self, state: AgentState) -> dict[str, Any]:
        """Runs the pricing engine and estimates business impact metrics."""
        # Calculate dynamic markup
        markup = 0.0
        reasons = []

        if state["occupancy_ratio"] > 0.85:
            markup += 0.20
            reasons.append("Occupancy forecast high (>85%)")
        elif state["occupancy_ratio"] < 0.40:
            markup -= 0.10
            reasons.append("Occupancy forecast low (<40%)")

        if state["is_peak_season"]:
            markup += 0.15
            reasons.append("Peak season event curves")

        # Cap markup according to policy documents if found
        if "30%" in state["policy_docs"]:
            markup = min(0.30, markup)
            reasons.append("Markup capped at 30% per hotel policy")

        # Estimate impact (mock calculation)
        projected_rev = 12000.0 * (1.0 + markup)
        expected_impact = {
            "projected_revenue_change": projected_rev - 12000.0,
            "projected_occupancy_change": -0.05 if markup > 0 else 0.0,
        }

        # Build Decision Package
        decision = DecisionPackage(
            decision_type="PRICING",
            prediction={
                "occupancy_ratio": state["occupancy_ratio"],
                "target_date": state["target_date"].date().isoformat(),
            },
            confidence=0.95,
            recommended_actions=[
                f"Adjust dynamic pricing rate markup to {int(markup * 100)}%"
            ],
            expected_business_impact=expected_impact,
            reasoning=reasons,
            supporting_evidence=["Local event scheduling", "Holiday weekend curves"],
            alternative_options=[
                {
                    "action": "Maintain base price",
                    "expected_impact": {"projected_revenue_change": 0.0},
                }
            ],
            risk_assessment={
                "risk_level": "LOW",
                "mitigation_plan": "Monitor real-time bookings daily",
            },
        )

        return {"decision_package": decision.model_dump()}

    async def explain_decision_node(self, state: AgentState) -> dict[str, Any]:
        """Generates natural language reasoning justifying the recommendation."""
        actions = state["decision_package"]["recommended_actions"]
        reasons = state["decision_package"]["reasoning"]
        impact = state["decision_package"]["expected_business_impact"]

        explanation = (
            f"Recommendation: {', '.join(actions)}. "
            f"This decision was formulated because: {', '.join(reasons)}. "
            f"Expected Impact: Projected revenue change is {impact['projected_revenue_change']:.2f}."
        )
        return {"explanation": explanation}

    async def run_workflow(
        self,
        room_category_id: uuid.UUID,
        target_date: datetime,
        occupancy_ratio: float,
        is_peak_season: bool = False,
    ) -> dict[str, Any]:
        """Runs the LangGraph decision orchestration workflow."""
        inputs = {
            "room_category_id": room_category_id,
            "target_date": target_date,
            "occupancy_ratio": occupancy_ratio,
            "is_peak_season": is_peak_season,
            "policy_docs": "",
            "decision_package": {},
            "explanation": "",
        }
        res = await self.graph.ainvoke(inputs)  # type: ignore[call-overload]
        return res  # type: ignore[no-any-return]
