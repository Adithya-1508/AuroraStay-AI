from collections.abc import Callable
from typing import Any

import structlog

from backend.agents.core.base_agent import (
    BaseAgent,
    ExecutionPlan,
    ExecutionResult,
)

logger = structlog.get_logger()


class AgentSupervisor:
    """Supervisor agent overseeing plan execution, error recovery, and metrics."""

    def __init__(self) -> None:
        self.metrics: dict[str, Any] = {
            "total_runs": 0,
            "failed_runs": 0,
            "recovery_attempts": 0,
            "successful_recoveries": 0,
        }

    async def oversee_execution(
        self,
        agent: BaseAgent,
        plan: ExecutionPlan,
        execute_fn: Callable[[ExecutionPlan], Any],
    ) -> ExecutionResult:
        """Oversees execution, triggering agent recovery routines on failures."""
        self.metrics["total_runs"] += 1
        logger.info(
            "Supervisor overseen execution start",
            agent=agent.name,
            plan_id=plan.plan_id,
        )

        try:
            result = await execute_fn(plan)
            assert isinstance(result, ExecutionResult)
            if result.success:
                logger.info(
                    "Supervisor overseen execution success",
                    agent=agent.name,
                    plan_id=plan.plan_id,
                )
                return result
            else:
                raise RuntimeError(result.error_message)
        except Exception as e:
            self.metrics["recovery_attempts"] += 1
            logger.warn(
                "Supervisor detected failure. Triggering agent recovery...",
                error=str(e),
            )

            # Trigger agent recovery hooks
            try:
                recovered = await agent.recover(e)
                if recovered:
                    self.metrics["successful_recoveries"] += 1
                    logger.info(
                        "Supervisor agent recovery succeeded. Retrying execution..."
                    )
                    # Re-run execution function after recovery
                    result = await execute_fn(plan)
                    assert isinstance(result, ExecutionResult)
                    return result
            except Exception as recovery_error:
                logger.error(
                    "Supervisor recovery hook exception", error=str(recovery_error)
                )

            self.metrics["failed_runs"] += 1
            logger.error(
                "Supervisor unrecoverable error: escalating failure.",
                agent=agent.name,
                plan_id=plan.plan_id,
            )
            return ExecutionResult(
                plan_id=plan.plan_id,
                success=False,
                error_message=f"Supervisor Escalated Failure: {e}",
            )


__all__ = ["AgentSupervisor"]
