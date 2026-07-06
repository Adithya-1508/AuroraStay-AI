import structlog

from backend.agents.core.base_agent import BaseAgent

logger = structlog.get_logger()


class AgentLifecycleMonitor:
    """Monitor class tracking and logging agent state transition events."""

    def log_transition(self, agent: BaseAgent, old_state: str, new_state: str) -> None:
        """Logs changes in agent states."""
        logger.info(
            "Agent state transition logged",
            agent_name=agent.name,
            old_state=old_state,
            new_state=new_state,
        )


__all__ = ["AgentLifecycleMonitor"]
