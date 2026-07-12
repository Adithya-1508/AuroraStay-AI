# Agent Monitoring Manual

## Overview
Agent Monitoring captures execution statistics for every autonomous agent in HospitalityAI. It tracks:
- **Planning Time**: Latency in ms for the agent to resolve prompt paths.
- **Execution Time**: Entire roundtrip invocation time.
- **Tool Usage**: Counts of individual tools triggered during resolving the query.
- **Decision Confidence**: The model's probability metrics on classification or recommendations.

## API Endpoint
- **GET** `/api/v1/observability/agents`
  - Returns a list of monitored agent execution structures.
