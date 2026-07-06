# Engineering Principles

Every engineering decision for HospitalityAI must align with these five principles.

## Principle 1: Business First
Technology exists to solve business problems.
- Every feature must have a measurable business objective.
- Never build technology for its own sake.

## Principle 2: Architecture Before Code
No production code may be written before architecture exists.
- Every significant feature requires an RFC, a design specification, and clear Acceptance Criteria.
- No hacky, undocumented bypasses are permitted.

## Principle 3: Quality Before Speed
Working software is not enough.
- Software must also be clean, readable, thoroughly tested, extensively documented, and maintainable.
- Refactor continuously and eliminate technical debt early.

## Principle 4: Everything is Observable
Every important operation must expose metrics, logs, traces, and health indicators.
- We must always know how the platform is performing.
- Telemetry must be structured and actionable.

## Principle 5: AI is a Component, not the Product
LLMs are only one part of the system.
- The platform should remain useful even if the LLM provider changes.
- Never tightly couple the application to a single model provider or proprietary SDK. Use clean abstractions and gateways.
