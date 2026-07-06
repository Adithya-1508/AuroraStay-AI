# Contributing to HospitalityAI

We welcome contributions! Please follow these steps to ensure a smooth merge process.

## 1. Branch and PR Rules
- Always branch from `develop`.
- Use the branching guidelines in [Git Workflow](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.foundation/git_workflow.md).
- Ensure all commits use Conventional Commit messages.

## 2. Coding Standards
- Run `make lint` and `make typecheck` before pushing changes.
- Ensure test coverage remains $\ge 90\%$.
- Exclude `TODO` comments from production modules.

## 3. Pull Request Checklist
Before submitting a PR, verify:
- [ ] Pre-commit hooks execute cleanly.
- [ ] Coverage requirements are met.
- [ ] Documentation updates are completed in the same commit.
