Version: 1.0

Status: Permanent

Applies To: Every Loop

Purpose

This document defines the immutable execution rules that govern every action performed by the autonomous coding agent throughout the HospitalityAI project.

If any loop conflicts with this document, this document takes precedence.

Rule 1

Never Guess.

If requirements are ambiguous:

Stop.

Explain the ambiguity.

Suggest possible approaches.

Wait for clarification.

Never invent requirements.

Rule 2

Architecture First.

Never implement code before:

RFC exists
ADR exists (if needed)
Acceptance Criteria exist
Rule 3

Always Preserve Existing Work.

Never delete:

files
modules
APIs
documentation

unless explicitly instructed.

Prefer incremental evolution over rewrites.

Rule 4

Never Break Existing Features.

Every implementation must preserve backward compatibility unless an approved ADR explicitly allows breaking changes.

Rule 5

Small Changes Win.

Prefer many small commits over one massive change.

Prefer incremental improvements.

Never perform repository-wide rewrites.

Rule 6

One Responsibility Per Module.

Every module should have one reason to change.

Avoid god objects.

Avoid giant files.

Avoid giant classes.

Rule 7

Business Logic Never Lives In Controllers.

Controllers only:

validate input
call services
return responses

Business rules belong in the domain/application layer.

Rule 8

Never Duplicate Logic.

Before implementing new functionality:

Search existing code.

Reuse existing modules.

Extract common behavior.

Rule 9

Everything Is Testable.

Every feature must be independently testable.

Avoid hidden dependencies.

Prefer dependency injection.

Rule 10

Prefer Composition.

Prefer

ReservationService

↓

PricingService

↓

AvailabilityService

instead of inheritance.

Rule 11

Every Public Function Needs Documentation.

Every public API

Every service

Every agent

Every module

must explain

purpose
inputs
outputs
exceptions
Rule 12

Errors Must Be Actionable.

Never

Something went wrong

Prefer

Reservation not found.

Reservation ID:

12345

Possible causes:

Reservation cancelled

Reservation deleted

Database unavailable
Rule 13

Logging Is Mandatory.

Every important action should log

who

what

when

where

why

Never log secrets.

Rule 14

Configuration Is External.

No

hardcoded URLs

hardcoded keys

hardcoded passwords

hardcoded model names

Everything belongs in configuration.

Rule 15

Provider Independence.

HospitalityAI must never depend on one

LLM

Vector DB

Cloud

Provider

Every provider must be replaceable.

Rule 16

AI Is Deterministic Where Possible.

Use

structured outputs

JSON schemas

tool calling

validation

Avoid free-form responses when deterministic behavior is possible.

Rule 17

Every Feature Has Documentation.

Feature complete means

Code

Tests

Docs

Examples

Rule 18

No TODOs In Production Code.

Temporary work must be tracked as GitHub Issues or RFCs.

Never leave TODO comments in production modules.

Rule 19

Refactor Continuously.

When duplication appears

Extract.

Simplify.

Improve naming.

Reduce complexity.

Rule 20

Security Is Default.

Validate every input.

Escape every output where needed.

Never trust user input.

Never expose internal errors.

Rule 21

Performance Comes Last.

Priority order

Correctness

↓

Maintainability

↓

Readability

↓

Testability

↓

Performance

Never optimize prematurely.

Rule 22

Everything Has An Owner.

Every

service

module

API

agent

must declare ownership inside documentation.

Rule 23

Every Decision Is Explainable.

When introducing

architecture

patterns

libraries

algorithms

document why.

Rule 24

Keep Humans In The Loop.

The coding agent must request approval before:

changing architecture
deleting code
introducing new dependencies
changing public APIs
changing database schemas
altering repository structure
Rule 25

Always Leave The Repository Better.

If a file is touched,

Improve it.

Fix formatting.

Improve naming.

Reduce duplication.

Update documentation.

Leave it cleaner than before.

Execution Contract

For every loop, Antigravity shall execute:

Read Constitution

↓

Read Execution Rules

↓

Read Current Loop

↓

Review Existing Repository

↓

Plan

↓

Implement

↓

Test

↓

Review

↓

Refactor

↓

Document

↓

Commit

↓

Report
Success Criteria

The repository should always remain in a deployable, well-documented, and testable state after each completed loop.

Rule 26

Specification First

No production implementation may begin until:

• Specification exists
• Specification reviewed
• Acceptance Criteria approved

If no specification exists:

STOP.

Generate one.

Request approval.

Only then continue.