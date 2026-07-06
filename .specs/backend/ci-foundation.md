# Spec: CI Foundation

- **Status**: Ready
- **Owner**: QA Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines build execution steps and validation checkers triggered in GitHub Actions.

## 2. CI Verification Pipeline
On pushes and PRs, the CI workflow must execute:
1. Check repository layout and config files.
2. Install Python runtime & `uv` package installer.
3. Validate coding style and formatting via Ruff.
4. Execute static typing validation via mypy.
5. Run the full test suite with coverage logs.
6. Verify docker compose file syntax.
