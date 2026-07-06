LOOP 00 — CONSTITUTION

Version: 1.0

Project: HospitalityAI

Execution Mode: Autonomous Engineering

Owner: Antigravity AI Coding Agent

Status: Mandatory

Mission

HospitalityAI is an enterprise-grade AI platform designed to improve hotel operations, automate business workflows, assist hotel staff, and enhance guest experiences through Artificial Intelligence, Machine Learning, Data Engineering, and Large Language Models.

This is not a demonstration project.

This is a production-quality software engineering project intended to showcase enterprise AI engineering practices.

Every engineering decision should optimize for:

Maintainability
Scalability
Reliability
Observability
Security
Developer Experience
Business Value
Vision

Build the most comprehensive open-source Hospitality AI platform demonstrating modern AI engineering.

The finished system should resemble software that could realistically be deployed inside a luxury hotel chain.

Engineering Philosophy

The project follows five engineering principles.

Principle 1

Business First

Technology exists to solve business problems.

Every feature must have a measurable business objective.

Never build technology for its own sake.

Principle 2

Architecture Before Code

No production code may be written before architecture exists.

Every significant feature requires:

RFC
Design
Acceptance Criteria
Principle 3

Quality Before Speed

Working software is not enough.

Software must also be:

readable
tested
documented
maintainable
Principle 4

Everything is Observable

Every important operation should expose

logs
metrics
traces
health
Principle 5

AI is a Component, not the Product

LLMs are only one part of the system.

The platform should remain useful even if the LLM provider changes.

Therefore:

Never tightly couple the application to a single model provider.

Product Objectives

The finished system should demonstrate expertise in:

AI Engineering
Agent Engineering
Backend Engineering
Machine Learning
Data Engineering
MLOps
API Design
Distributed Systems
Production Deployment
Success Metrics

The project is successful when it demonstrates:

Enterprise-grade architecture
Production-quality code
Complete documentation
Automated testing
CI/CD
Reproducible deployment
AI agents solving realistic hotel workflows
Clean developer experience
Non-Goals

The project is NOT intended to:

become a commercial SaaS
support payment processing
integrate with real hotel systems
handle production traffic
support thousands of concurrent users

Mock integrations are acceptable where appropriate.

Engineering Standards

Every line of code must satisfy the following priorities.

Correctness
Simplicity
Readability
Maintainability
Performance

Never sacrifice readability for micro-optimizations.

Coding Standards

Mandatory:

Python 3.12+
Type hints everywhere
Async-first architecture
Pydantic v2
SQLAlchemy 2.x
Ruff
Black
mypy
pytest

Forbidden:

global mutable state
circular imports
duplicated logic
hardcoded secrets
giant functions
magic numbers
commented-out code
dead code
Repository Rules

Every module must have a single responsibility.

Example:

agents/
backend/
ml/
etl/
dashboard/
shared/
tests/
docs/

No module may exceed its defined responsibility.

Branch Strategy

Main

↓

Develop

↓

Feature Branch

↓

Pull Request

↓

Review

↓

Merge

Never commit directly to main.

Git Commit Convention

Use Conventional Commits.

Examples:

feat(agent): add reservation planner

fix(etl): handle null booking dates

docs(api): update reservation endpoints

test(ml): add occupancy prediction tests

refactor(core): simplify dependency injection
Definition of Ready (DoR)

A feature is ready for implementation only if it has:

Business objective
RFC
Acceptance criteria
API design (if applicable)
Data model (if applicable)
Test strategy
Dependencies identified
Definition of Done (DoD)

A feature is complete only when:

Implementation finished
Unit tests pass
Integration tests pass
Ruff passes
mypy passes
Documentation updated
OpenAPI updated
Logging added
Error handling implemented
Code reviewed
Acceptance criteria satisfied
Documentation Rules

Every feature updates:

README
API docs
Architecture docs (if affected)
ADR (if architectural decisions change)
RFC status

Documentation is part of the feature—not a later task.

Testing Strategy

Minimum requirements:

Unit tests for business logic
Integration tests for APIs
End-to-end tests for critical workflows
AI evaluation tests for agent behavior
Regression tests for bug fixes

Target code coverage: ≥ 90%.

Security Principles

The project must:

Validate all inputs
Use JWT authentication
Implement role-based access control
Store secrets in environment variables
Log security-relevant events
Prevent SQL injection through ORM usage
Apply rate limiting to public APIs
AI Engineering Principles

The AI layer must be:

Provider-agnostic
Deterministic where possible
Observable
Evaluated
Testable

Prompts should be version-controlled and reusable.

Every agent must declare:

Role
Goal
Tools
Memory strategy
Failure handling
Success criteria
Architecture Rules

The project follows layered architecture:

Presentation Layer
        │
Application Layer
        │
Domain Layer
        │
Infrastructure Layer

Business logic must never live in controllers or API routes.

Quality Gates

No loop may be marked complete unless:

All tests pass
Linting passes
Type checking passes
Docker builds successfully
Documentation is current
Acceptance criteria are met
Autonomous Agent Rules

Antigravity must:

Never skip a loop.
Never implement features without an approved specification.
Never invent business requirements—ask for clarification if they're missing.
Prefer modular, reusable components over one-off implementations.
Treat generated code as production-ready, not prototype code.
Preserve backward compatibility unless an approved architectural change (ADR) justifies breaking it.
Explain significant design decisions in ADRs.
Pause implementation and report blockers instead of guessing when requirements are ambiguous.
Exit Criteria for Loop 00

Loop 00 is complete only when:

Engineering Constitution finalized.
Coding standards defined.
Repository governance established.
Quality gates documented.
Definition of Ready and Definition of Done approved.
Branching, testing, and documentation policies established.
Engineering principles accepted as mandatory for all future loops.
Deliverables

At the end of Loop 00, the repository should contain only foundational documentation, such as:

.foundation/
    constitution.md
    engineering_principles.md
    coding_standards.md
    quality_gates.md
    git_workflow.md
    definition_of_done.md
    definition_of_ready.md
    security_principles.md

Repository Standards

↓

.specs is the canonical implementation specification directory.

Every feature requiring implementation must have a corresponding specification before coding begins.    

No application code should exist after Loop 00. The sole purpose of this loop is to establish the rules that govern every engineering decision in the project. Once these documents are complete and accepted, the project can move to Loop 01 – Product Requirements & Discovery.