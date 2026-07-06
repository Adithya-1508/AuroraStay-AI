# Quality Gates

No loop or feature may be merged, deployed, or marked complete without passing all of the following gates.

## 1. Automated Verification
- **Test Pass Rate**: 100% of unit, integration, and end-to-end tests must pass.
- **Code Coverage**: Total code coverage must be $\ge 90\%$.
- **Linting**: Ruff formatting and linting must pass with zero issues.
- **Type Checking**: Mypy must pass in strict mode with zero typing errors.

## 2. Platform Build
- **Containerization**: The system's Dockerfiles and orchestration configs (e.g. `docker-compose`) must build successfully with zero errors or warnings.

## 3. Product & Governance Compliance
- **Acceptance Criteria**: Every acceptance criteria documented in the specifications/loops must be fully met.
- **Documentation**: All public APIs, services, and modules must have accurate, current documentation. README and OpenAPI specs must be in sync with the codebase.
- **No TODOs**: Zero `TODO` or `FIXME` comments can exist in production code.

## 4. Performance & Security
- **API Latency**: Must meet targets specified in non-functional requirements.
- **Input Validation**: All APIs must validate input schema using Pydantic.
