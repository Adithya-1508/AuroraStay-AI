from typing import Any

from backend.agents.core.base_agent import (
    BaseAgent,
    ExecutionPlan,
    ExecutionResult,
)
from backend.agents.executor.service import AgentExecutor
from backend.agents.graph.engine import GraphState, WorkflowEngine
from backend.agents.planner.service import AgentPlanner
from backend.ai.cache.semantic import AICache
from backend.ai.models.registry import ModelRegistry
from backend.ai.prompts.registry import PromptRegistry
from backend.ai.providers.registry import ProviderRegistry
from backend.ai.routing.router import ModelRouter
from backend.ai.service import AIService
from backend.ai.telemetry.tracker import AITelemetryTracker
from backend.ai.tools.executor import ToolExecutor
from business.guest.workflows.tools import (
    EscalateToStaffTool,
    FindRestaurantTool,
    FindSpaServiceTool,
    GuestPreferenceTool,
    RecommendFacilityTool,
    ReservationLookupTool,
    SearchHotelKnowledgeTool,
)


class GuestConciergeAgent(BaseAgent):
    """Business AI Agent acting as a luxury concierge for hotel guests."""

    name = "GuestConcierge"
    version = "1.0.0"
    description = "AI Concierge Agent assisting guests with FAQs, recommendations, dining, spa booking, and escalations."
    owner = "Domain Engineering Team"

    capabilities = [
        "Search hotel policy and FAQs",
        "Find restaurant dining choices",
        "Find spa services and activities",
        "Recommend personalized facilities",
        "Look up guest reservations",
        "Update guest stay preferences",
        "Escalate requests to hotel staff",
    ]

    required_tools = [
        "SearchHotelKnowledgeTool",
        "FindRestaurantTool",
        "FindSpaServiceTool",
        "RecommendFacilityTool",
        "ReservationLookupTool",
        "GuestPreferenceTool",
        "EscalateToStaffTool",
    ]

    supported_workflows = [
        "Query Policy FAQ",
        "Browse Dining Menu",
        "Browse Spa Menu",
        "Get Suggestions",
        "Query Reservations",
        "Modify Preference",
        "Staff Handoff",
    ]

    async def _on_initialize(self) -> None:
        """Sets up the AI service adapters, tool executors, and LangGraph workflow engine."""
        self.providers = ProviderRegistry()
        self.models = ModelRegistry()
        self.router = ModelRouter(self.models)
        self.prompts = PromptRegistry()
        self.cache = AICache()
        self.telemetry = AITelemetryTracker()

        self.ai_service = AIService(
            self.providers,
            self.models,
            self.router,
            self.prompts,
            self.cache,
            self.telemetry,
        )

        self.tool_instances = [
            SearchHotelKnowledgeTool(),
            FindRestaurantTool(),
            FindSpaServiceTool(),
            RecommendFacilityTool(),
            ReservationLookupTool(),
            GuestPreferenceTool(),
            EscalateToStaffTool(),
        ]
        self.tool_executor = ToolExecutor(self.tool_instances)

        self.planner = AgentPlanner(self.ai_service)
        self.executor = AgentExecutor(self.tool_executor)
        self.engine = WorkflowEngine(self.planner, self.executor)

    async def _on_plan(self, goal: str) -> ExecutionPlan:
        """Decomposes goals using the planner service."""
        return await self.planner.create_plan(goal, self.required_tools)

    async def _on_execute(self, plan: ExecutionPlan) -> ExecutionResult:
        """Delegates plan execution to the agent executor service."""
        return await self.executor.execute_plan(plan)

    async def chat(
        self, session_id: str, message: str, thread_id: str | None = None
    ) -> dict[str, Any]:
        """Allows direct conversational chats running LangGraph execution states."""
        t_id = thread_id or f"chat-thread-{session_id}"
        config = {"configurable": {"thread_id": t_id}}

        initial_state: GraphState = {
            "thread_id": t_id,
            "goal": message,
            "tools": self.required_tools,
            "plan_steps": [],
            "completed_steps": [],
            "current_step_idx": 0,
            "paused": False,
            "requires_approval": False,
            "approval_given": False,
            "error": None,
            "step_results": {},
            "success": False,
        }

        state = await self.engine.graph.ainvoke(initial_state, config)  # type: ignore[call-overload]

        return {
            "thread_id": state.get("thread_id"),
            "success": state.get("success"),
            "paused": state.get("paused"),
            "requires_approval": state.get("requires_approval"),
            "completed_steps": state.get("completed_steps"),
            "step_results": state.get("step_results"),
            "error": state.get("error"),
        }


__all__ = ["GuestConciergeAgent"]
