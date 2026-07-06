# ADR-0004: Multi-Agent Orchestration Framework Selection

- **Status**: Approved
- **Date**: 2026-07-04
- **Author**: Antigravity AI Coding Agent
- **Owner**: Agent Platform
- **Supersedes**: None

## Context
HospitalityAI's conversational workflows are complex: they involve routing guest queries between general FAQs, booking engines, and staff escalations. Managing this logic with simple system prompts or basic linear LLM chains is fragile. We need a stateful framework that supports cycles, tool execution feedback loops, and human-in-the-loop interventions.

## Decision
We select **LangGraph** (by LangChain) as the core multi-agent orchestration framework.
- Agents, planners, and executors will be defined as graph nodes.
- Redis will act as the state checkpoints persistence layer.

## Rationale
- **Stateful Cyclic Flows**: LangGraph is designed around cycles (e.g. LLM -> Call Tool -> Check Output -> LLM again), which are critical for agent reasoning, whereas most frameworks only support Directed Acyclic Graphs (DAGs).
- **Human-in-the-Loop native support**: Provides native breakpoints to pause graph execution and await human confirmation (e.g., prior to cancelling a room).
- **Control and Predictability**: Unlike agent frameworks that use autonomous, free-roaming loops, LangGraph lets developers define explicit graph edges and routing conditions, making execution paths predictable and verifiable.

## Alternatives Considered
- **CrewAI / AutoGen**: Evaluated. While powerful, they rely on autonomous agent conversations, which are highly non-deterministic, hard to validate, prone to infinite token-spending loops, and lack first-class support for explicit cyclic flows.
- **Custom Python State Machines**: Writing raw state machines is highly reliable but forces us to implement state serializations, checkpointing, and tool-invocation history logs from scratch.

## Consequences
- **Pros**:
  - Predictable agent routing.
  - Native support for tool calls and human validation.
- **Cons/Risks**:
  - Higher learning curve compared to simple sequential chains.
- **Migration/Rollout**:
  - LangGraph nodes and supervisors will be implemented in Loop 08.
