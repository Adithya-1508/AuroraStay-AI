# Agent Platform: Planner

This document describes the task decomposition mechanics.

## Operation Mode

The `AgentPlanner` acts as an offline planning unit:
1. Receives input goal strings and lists of allowable tool names.
2. Formulates query prompts asking the LLM to output structured plan steps and dependency ordering.
3. Compiles the response into an `ExecutionPlan`.
4. If the AI service is disabled or errors, defaults to sequential step chains to protect flow stability.
