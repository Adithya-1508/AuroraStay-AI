import json
from uuid import uuid4

from backend.agents.core.base_agent import ExecutionPlan, ExecutionStep
from backend.ai.service import AIService


class AgentPlanner:
    """Planner decomposing user goals into a list of plan steps with dependencies."""

    def __init__(self, ai_service: AIService | None = None) -> None:
        self.ai_service = ai_service

    async def create_plan(self, goal: str, available_tools: list[str]) -> ExecutionPlan:
        """Decomposes user goal, resolving step dependency hierarchies."""
        plan_id = str(uuid4())

        if not self.ai_service:
            # Heuristic/mock fallback for unit test isolation
            steps = []
            dependencies = {}
            prev_id = None
            for idx, tool in enumerate(available_tools):
                step_id = f"step_{idx + 1}"
                steps.append(
                    ExecutionStep(
                        step_id=step_id,
                        name=f"run_{tool}",
                        tool=tool,
                        arguments={"goal": goal},
                    )
                )
                if prev_id:
                    dependencies[step_id] = [prev_id]
                prev_id = step_id
            return ExecutionPlan(
                plan_id=plan_id, steps=steps, dependencies=dependencies
            )

        prompt = (
            f"Decompose the following goal: '{goal}' into plan steps. "
            f"Available tools: {available_tools}. "
            f"Return a JSON dict with keys 'steps' and 'dependencies'. "
            f"Each step must have 'name', 'tool', and 'arguments'."
        )

        try:
            res = await self.ai_service.generate(
                messages=[{"role": "user", "content": prompt}], task="planning"
            )
            # Find and extract JSON block
            content = res.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            data = json.loads(content.strip())
            steps = []
            for idx, s in enumerate(data.get("steps", [])):
                step_id = s.get("step_id") or f"step_{idx + 1}"
                steps.append(
                    ExecutionStep(
                        step_id=step_id,
                        name=s["name"],
                        tool=s["tool"],
                        arguments=s.get("arguments", {}),
                    )
                )
            return ExecutionPlan(
                plan_id=plan_id,
                steps=steps,
                dependencies=data.get("dependencies", {}),
            )
        except Exception:
            # Fallback to sequential dependencies if LLM routing/parsing fails
            steps = []
            dependencies = {}
            prev_id = None
            for idx, tool in enumerate(available_tools):
                step_id = f"step_{idx + 1}"
                steps.append(
                    ExecutionStep(
                        step_id=step_id,
                        name=f"run_{tool}",
                        tool=tool,
                        arguments={"goal": goal},
                    )
                )
                if prev_id:
                    dependencies[step_id] = [prev_id]
                prev_id = step_id
            return ExecutionPlan(
                plan_id=plan_id, steps=steps, dependencies=dependencies
            )


__all__ = ["AgentPlanner"]
