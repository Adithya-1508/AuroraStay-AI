# Git Workflow

A disciplined branching and commit model is essential for maintaining a clean, auditable repository.

## Branch Strategy

We use a structured branch flow:

```
Main (Production Release)
  ▲
  │ (Release / Tag)
Develop (Integration Branch)
  ▲
  │ (Pull Request / Squash Merge)
Feature / Bugfix / Refactor Branches
```

1. **Main**: Production-ready code. Never commit directly to `main`.
2. **Develop**: Integration branch for currently working features.
3. **Feature Branch**: Created from `develop` for specific user stories or bug fixes (e.g., `feat/reservation-planner` or `fix/etl-null-dates`).

## Commit Convention
We strictly follow **Conventional Commits 1.0.0**. Commits must use the following format:
`<type>(<scope>): <description>`

Common types:
- `feat`: A new user-facing feature.
- `fix`: A bug fix.
- `docs`: Documentation-only changes.
- `test`: Adding missing tests or correcting existing tests.
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `chore`: Updates to build scripts, configurations, or CI pipelines.

Examples:
- `feat(agent): add reservation planner`
- `fix(etl): handle null booking dates`
- `docs(api): update reservation endpoints`
- `test(ml): add occupancy prediction tests`
- `refactor(core): simplify dependency injection`
