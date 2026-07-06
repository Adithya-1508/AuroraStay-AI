# AI Platform Specification: AI Evaluation & Regression Testing

## Overview
Defines frameworks to measure prompt quality, track regression, and run automated benchmarking.

## Evaluation Structures
- **Golden Dataset**: Map collection of test cases `[{"input": dict, "expected_contains": list[str], "min_score": float}]`.
- **Evaluator Orchestrator**:
  - Executes prompt templates against target models.
  - Scores responses against golden expectations using keyword presence, token count boundaries, or custom scoring logic.
  - Generates evaluation run reports outlining pass/fail status and average latencies.
