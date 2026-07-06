from typing import Any

from backend.agents.core.base_agent import (
    ExecutionPlan,
    ExecutionResult,
    ExecutionStep,
)
from backend.ai.tools.executor import ToolExecutor


class AgentExecutor:
    """Executor executing plan steps sequentially with dependency resolution."""

    def __init__(self, tool_executor: ToolExecutor) -> None:
        self.tool_executor = tool_executor

    async def execute_step(
        self, step: ExecutionStep, caller_permissions: list[str] | None = None
    ) -> Any:
        """Executes a single step, routing to ToolExecutor with retries checks."""
        step.status = "RUNNING"
        attempt = 0
        last_err = None

        while attempt <= step.max_retries:
            try:
                res = await self.tool_executor.execute(
                    tool_name=step.tool,
                    arguments=step.arguments,
                    caller_permissions=caller_permissions,
                )
                step.status = "SUCCESS"
                step.result = res
                return res
            except Exception as e:
                attempt += 1
                step.retries = attempt
                last_err = str(e)
                if attempt > step.max_retries:
                    step.status = "FAILED"
                    step.error = last_err
                    raise e

    async def execute_plan(
        self, plan: ExecutionPlan, caller_permissions: list[str] | None = None
    ) -> ExecutionResult:
        """Executes all steps, mapping topological dependency sequence ordering."""
        results = {}
        completed: set[str] = set()

        dependencies = dict(plan.dependencies)

        while len(completed) < len(plan.steps):
            ready_steps = []
            for s in plan.steps:
                if s.step_id in completed:
                    continue
                prereqs = dependencies.get(s.step_id, [])
                if all(p in completed for p in prereqs):
                    ready_steps.append(s)

            if not ready_steps:
                return ExecutionResult(
                    plan_id=plan.plan_id,
                    success=False,
                    error_message="Deadlock: dependency cycle detected in plan.",
                )

            for step in ready_steps:
                try:
                    res = await self.execute_step(
                        step, caller_permissions=caller_permissions
                    )
                    results[step.step_id] = res
                    completed.add(step.step_id)
                except Exception as e:
                    return ExecutionResult(
                        plan_id=plan.plan_id,
                        success=False,
                        step_results=results,
                        error_message=f"Step '{step.step_id}' failed: {e}",
                    )

        return ExecutionResult(plan_id=plan.plan_id, success=True, step_results=results)


__all__ = ["AgentExecutor"]
