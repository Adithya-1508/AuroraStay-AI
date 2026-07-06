# Spec: Developer Tooling

- **Status**: Ready
- **Owner**: QA Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Ruff Linting and Formatting
- Format Check: Runs `ruff format --check .`.
- Lint Check: Enforces coding standards configured in [pyproject.toml](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/pyproject.toml).

## 2. mypy Typing Checks
- All code files must resolve type validation cleanly under strict check conditions (`strict = true`).

## 3. pytest Testing Framework
- Runner must verify unit/integration tests and generate coverage metrics.
- Code coverage target is set to $\ge 90\%$.
