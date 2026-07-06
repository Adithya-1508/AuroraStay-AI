# Developer Tooling Standards

This document describes the validation checkers enforced locally and in our CI system.

## 1. Ruff (Linter and Formatter)
- Enforces UP (upgrade), I (isort), E/W (pycodestyle), F (pyflakes), B (bugbear), and S (security/bandit) rules.
- Run Ruff via:
  ```bash
  ruff check .
  ruff format --check .
  ```

## 2. mypy (Static Type Checker)
- Run type validation in strict mode:
  ```bash
  mypy shared tests
  ```

## 3. pytest (Test Framework)
- Execute unit and integration tests with coverage reporting:
  ```bash
  pytest
  ```
- Target coverage: $\ge 90\%$.
