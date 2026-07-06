from typing import Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from backend.agents.core.base_agent import ExecutionPlan, ExecutionStep
from backend.agents.executor.service import AgentExecutor
from backend.agents.planner.service import AgentPlanner


class GraphState(TypedDict):
    """LangGraph state representation dictionary."""

    thread_id: str
    goal: str
    tools: list[str]
    plan_steps: list[dict[str, Any]]
    completed_steps: list[str]
    current_step_idx: int
    paused: bool
    requires_approval: bool
    approval_given: bool
    error: str | None
    step_results: dict[str, Any]
    success: bool


class WorkflowEngine:
    """Core LangGraph Workflow Engine compiling agent state routing DAGs."""

    def __init__(self, planner: AgentPlanner, executor: AgentExecutor) -> None:
        self.planner = planner
        self.executor = executor

        # Build graph configuration
        builder = StateGraph(GraphState)

        # Register execution nodes
        builder.add_node("planner_node", self.planner_node)
        builder.add_node("executor_node", self.executor_node)
        builder.add_node("human_approval_node", self.human_approval_node)
        builder.add_node("supervisor_node", self.supervisor_node)

        # Declare transition edges
        builder.add_edge(START, "planner_node")
        builder.add_edge("planner_node", "executor_node")

        builder.add_conditional_edges(
            "executor_node",
            self.route_after_execution,
            {"approval": "human_approval_node", "supervisor": "supervisor_node"},
        )

        builder.add_edge("human_approval_node", "supervisor_node")

        builder.add_conditional_edges(
            "supervisor_node",
            self.route_after_supervision,
            {"execute": "executor_node", "end": END},
        )

        # Memory Checkpointer for LangGraph thread snapshots
        self.checkpointer = MemorySaver()
        self.graph = builder.compile(
            checkpointer=self.checkpointer,
            interrupt_before=["human_approval_node"],
        )

    async def planner_node(self, state: GraphState) -> dict[str, Any]:
        """Invokes planner agent decomposing target goals."""
        plan: ExecutionPlan = await self.planner.create_plan(
            state["goal"], state["tools"]
        )
        serialized_steps = [
            {
                "step_id": s.step_id,
                "name": s.name,
                "tool": s.tool,
                "arguments": s.arguments,
                "status": s.status,
                "retries": s.retries,
                "max_retries": s.max_retries,
            }
            for s in plan.steps
        ]
        return {
            "plan_steps": serialized_steps,
            "current_step_idx": 0,
            "completed_steps": [],
            "error": None,
        }

    async def executor_node(self, state: GraphState) -> dict[str, Any]:
        """Node executing the current step in the plan list."""
        steps = state["plan_steps"]
        idx = state["current_step_idx"]

        if idx >= len(steps):
            return {"success": True}

        step_data = steps[idx]
        step = ExecutionStep(
            step_id=step_data["step_id"],
            name=step_data["name"],
            tool=step_data["tool"],
            arguments=step_data["arguments"],
            status=step_data["status"],
            retries=step_data["retries"],
            max_retries=step_data["max_retries"],
        )

        # Identify sensitive actions needing human confirmations approval
        needs_approval = step.tool.startswith("delete") or step.tool.startswith(
            "confirm"
        )
        if needs_approval and not state.get("approval_given"):
            return {"requires_approval": True, "paused": True}

        try:
            res = await self.executor.execute_step(step)
            step_results = dict(state.get("step_results") or {})
            step_results[step.step_id] = res

            completed = list(state.get("completed_steps") or [])
            completed.append(step.step_id)

            steps[idx]["status"] = "SUCCESS"
            steps[idx]["result"] = res

            return {
                "plan_steps": steps,
                "current_step_idx": idx + 1,
                "completed_steps": completed,
                "step_results": step_results,
                "approval_given": False,
                "requires_approval": False,
                "paused": False,
            }
        except Exception as e:
            steps[idx]["status"] = "FAILED"
            steps[idx]["error"] = str(e)
            return {"plan_steps": steps, "error": str(e)}

    async def human_approval_node(self, state: GraphState) -> dict[str, Any]:
        """Interrupt node halting execution thread awaiting approvals input."""
        return {"paused": False, "requires_approval": False}

    async def supervisor_node(self, state: GraphState) -> dict[str, Any]:
        """Verifies plan execution success and monitors bounds check constraints."""
        if state.get("error"):
            return {"success": False}

        idx = state["current_step_idx"]
        steps = state["plan_steps"]

        if idx >= len(steps):
            return {"success": True}

        return {}

    def route_after_execution(self, state: GraphState) -> str:
        """Branches routes into human approvals or supervisor checks."""
        if state.get("requires_approval") and state.get("paused"):
            return "approval"
        return "supervisor"

    def route_after_supervision(self, state: GraphState) -> str:
        """Decides if the workflow completes or executes the next step."""
        if state.get("error") or state.get("success"):
            return "end"
        return "execute"


__all__ = ["GraphState", "WorkflowEngine"]
