LOOP 05 — Backend Core Platform

Version: 1.0

Project: HospitalityAI

Status: Mandatory

Prerequisites

Loop 00 — Constitution
Loop 01 — Product Requirements
Loop 02 — Architecture
Loop 03 — Domain Model
Loop 04 — Repository Bootstrap
Purpose

Build the backend foundation that every future module depends on.

This loop does NOT implement business features like Reservations or AI Concierge.

Instead, it creates the backend framework that all future services plug into.

Think of this as building Spring Boot or Django before writing business logic.

Goal

Create a production-ready FastAPI backend that includes:

Dependency Injection
Configuration
Authentication Framework
Authorization
Error Handling
Logging
Middleware
Versioned APIs
Health Monitoring
OpenAPI
Base Models
Repository Interfaces

No hotel business logic should exist after this loop.

Deliverables

Create

backend/

├── app/
│
├── api/
│   ├── v1/
│   ├── dependencies.py
│   ├── router.py
│   └── middleware.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── logging.py
│   ├── settings.py
│   ├── lifecycle.py
│   └── constants.py
│
├── auth/
│   ├── jwt.py
│   ├── permissions.py
│   ├── roles.py
│   ├── password.py
│   └── middleware.py
│
├── exceptions/
│
├── schemas/
│
├── services/
│
├── repositories/
│
├── models/
│
├── middleware/
│
├── telemetry/
│
├── health/
│
├── dependencies/
│
└── main.py
Backend Architecture

Must follow

API

↓

Application Services

↓

Domain Interfaces

↓

Infrastructure

↓

Database

Forbidden

API

↓

Database

Business logic never belongs inside API routes.

FastAPI

Configure

lifespan
dependency injection
startup hooks
shutdown hooks
OpenAPI metadata
API versioning
Dependency Injection

Create a centralized DI system.

Services should never instantiate repositories directly.

Example

ReservationService

↓

ReservationRepository

↓

Database

Use FastAPI Depends or a dedicated DI layer.

Configuration

Implement a configuration system using Pydantic Settings.

Support

Development
Testing
Production

Configuration must be immutable after startup.

Authentication

Implement JWT infrastructure.

Do NOT implement login yet.

Only create

token generation
token validation
user context extraction
role extraction
Authorization

Design RBAC.

Roles

Guest

Staff

Manager

Administrator

AI Service

Worker

Permissions should be policy-based.

Middleware

Create middleware for

Request Logging

Correlation IDs

Error Handling

Request Timing

Rate Limiting (stub)

Security Headers

CORS

Compression

Every request receives a unique Request ID.

Error Handling

Create a global exception framework.

Support

Validation Errors

Authentication Errors

Authorization Errors

Business Errors

Infrastructure Errors

Unknown Errors

Every error returns

Error Code

Message

Correlation ID

Timestamp
Logging

Structured JSON logging.

Every request logs

Method

Path

Status

Latency

Request ID

Never log secrets.

Health

Endpoints

GET /health

GET /ready

GET /live

Each endpoint should report:

Database

Redis

Vector DB

LLM Provider

Overall status

API Versioning

Create

/api/v1

Future versions

/api/v2

No endpoint outside versioning.

OpenAPI

Customize

Title

Description

Tags

Authentication

Examples

Error Responses

Response Model

Every response follows

{
  "success": true,
  "data": {},
  "metadata": {},
  "request_id": "",
  "timestamp": ""
}

Every error follows

{
  "success": false,
  "error": {
    "code": "",
    "message": ""
  },
  "request_id": "",
  "timestamp": ""
}
Repository Pattern

Create abstract repositories.

No SQL yet.

Only interfaces.

Example

GuestRepository

ReservationRepository

ReviewRepository

KnowledgeRepository

Implementation comes later.

Base Models

Create reusable

BaseEntity

TimestampMixin

UUIDMixin

SoftDeleteMixin

AuditMixin

No business entities yet.

Security

Implement

JWT validation

Password hashing

Secrets management

Request validation

Input sanitization

Security headers

No authentication endpoints.

Telemetry

Prepare

Prometheus

OpenTelemetry

Metrics Registry

Tracing

Only infrastructure.

Testing

Create tests for

Configuration

Middleware

Authentication

Authorization

Health endpoints

Dependency injection

Error handling

Coverage target

95%

Documentation

Generate

docs/api/

authentication.md

middleware.md

error-handling.md

response-format.md

backend-architecture.md
Quality Gates

Loop fails if

❌ Business logic exists

❌ Reservation endpoints exist

❌ AI endpoints exist

❌ Database models exist

❌ SQL queries exist

Those belong to later loops.

Acceptance Criteria

The backend should

✅ Start successfully

✅ Return health checks

✅ Generate OpenAPI

✅ Authenticate JWT

✅ Produce structured logs

✅ Handle exceptions

✅ Validate requests

✅ Support dependency injection

✅ Support versioned APIs

✅ Pass all tests

Definition of Done

Loop 05 is complete only when

FastAPI backend is production-ready.
Authentication infrastructure exists.
Middleware pipeline exists.
Global exception handling exists.
Dependency injection exists.
Health monitoring exists.
OpenAPI documentation is generated.
Testing passes.
No business modules have been implemented.
Exit Criteria

HospitalityAI now has an enterprise-grade backend platform ready for feature development.

From this point onward, every business capability (Reservations, AI Concierge, ETL, ML, etc.) will plug into this foundation rather than reinventing backend infrastructure.

Engineering Note for Antigravity

Before implementing anything in this loop, Antigravity must:

Instead of directly implementing backend,

Loop 05 should first generate

.specs/backend/

api.md

middleware.md

authentication.md

dependency-injection.md

logging.md

error-handling.md

configuration.md

Only then implement them.

Read Loop 00 (Constitution).
Read execution-rules.md.
Read Loops 01–04 for context.
Review the existing repository.
Produce an implementation plan before writing code.
Execute work in small, reviewable commits.
Verify all quality gates before marking the loop complete