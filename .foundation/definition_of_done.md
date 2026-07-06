# Definition of Done (DoD)

A user story, task, or bug fix is considered complete **only** when it meets all of the following requirements:

## 1. Code Quality
- [ ] Code compiles and contains no syntax or logic errors.
- [ ] No `TODO`, `FIXME`, or temporary code remains in production modules.
- [ ] All code conforms to [Coding Standards](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.foundation/coding_standards.md).
- [ ] Ruff linting and formatting checks pass.
- [ ] Mypy strict type-checking passes.

## 2. Testing
- [ ] Unit tests written for all new business logic.
- [ ] Integration tests written for all new API endpoints.
- [ ] All tests run and pass successfully.
- [ ] Total project test coverage remains $\ge 90\%$.

## 3. Operations & Observability
- [ ] Actionable error handling is implemented.
- [ ] Structured logging is added for major system events (who, what, when, where, why).
- [ ] Metrics/Traces are registered (if applicable).

## 4. Documentation
- [ ] Inline code comments and docstrings updated for public interfaces.
- [ ] OpenAPI (Swagger) schema is updated and valid.
- [ ] High-level design documents / specs updated.
- [ ] Project README updated.

## 5. Review & Approval
- [ ] Code is reviewed and approved.
- [ ] All Acceptance Criteria defined in the specification are fully satisfied.
