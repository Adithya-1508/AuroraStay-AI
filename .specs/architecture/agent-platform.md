# Spec: Agent Platform & LangGraph Orchestration

- **Status**: Ready
- **Owner**: Agent Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the multi-agent orchestration states, supervisor router configurations, tools calling engines, and runaway recursion checks.

## 2. Responsibilities
- Coordinate agent tasks utilizing stateful graphs (LangGraph).
- Classify incoming messages to route tasks to appropriate sub-agents.
- Intercept agent execution states to monitor loop recursion counts.
- Manage execution states using Redis-backed transaction checks.
- Detect handoff events and alert human operators.

## 3. Dependencies
- **LangGraph / LangChain**: Underlying stateful multi-agent framework.
- **AI Platform**: For token validation and LLM adapter endpoints.
- **Redis**: For managing conversation history and session states.

## 4. Public Interfaces
```python
# Declarations of state schema and router

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_agent: str
    session_id: str
    correlation_id: str
    recursion_count: int

class AgentSupervisor:
    def compile_graph(self) -> CompiledGraph:
        """Assembles agents, router, and tool nodes into a stateful graph."""
        pass
```

## 5. Configuration
- `MAX_RECURSION_LIMIT`: Safety cutoff iteration count (default: `15`).
- `AGENT_TIMEOUT_SECONDS`: Execution timeout limit (default: `30`).

## 6. Failure Modes
- **Runaway Agent Loop**: If the execution recursion reaches `MAX_RECURSION_LIMIT`, raise `AgentLoopException`, log a warning, and fall back to front desk handoff.
- **Tool Execution Exceptions**: If a tool fails (e.g. database locks during reservation creation), capture the exception, return the error details to the planner agent, and request corrective actions.

## 7. Security Considerations
- Validate user permissions before allowing the planner to trigger specific tool calls.
- Enforce output schema validation to prevent LLM code injections.

## 8. Testing Strategy
- **Unit Tests**: Test the graph structure with mock tools to verify that routing states (FAQ vs Reservation) trigger correctly.
- **Evaluation Tests**: Run representative prompt sequences to verify that the agent graph completes within targets and invokes expected tools.
