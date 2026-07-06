# Coding Workflow Instructions

Follow this workflow to submit code changes.

## 1. Local Branch Creation
- Checkout the `develop` branch:
  ```bash
  git checkout develop
  git pull origin develop
  ```
- Create a feature branch:
  ```bash
  git checkout -b feature/your-feature-name
  ```

## 2. Commit Rules
Commits must conform to Conventional Commits:
- `feat: add room checkout triggers`
- `fix: correct price calculation overlap`
- `docs: update setup documentation`

## 3. Pull Request Submission
- Ensure all quality gates (`make lint`, `make typecheck`, `make test`) pass locally.
- Submit a PR targeting the `develop` branch.
- Wait for reviews and green light checks from the CI validation pipeline.
