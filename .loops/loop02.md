LOOP 02 — SYSTEM ARCHITECTURE

Version: 1.0

Prerequisites:

Loop 00 completed
Loop 01 completed

Status:

Mandatory

Purpose

Design the complete architecture of HospitalityAI before any implementation begins.

This loop defines how the system is built.

No implementation code may be written in this loop.

This loop establishes:

system boundaries
service decomposition
data flow
AI architecture
ML architecture
deployment architecture
integration strategy

Everything built later must follow this architecture.

Philosophy

Architecture exists to reduce complexity.

The architecture must optimize for

maintainability
scalability
modularity
observability
developer experience
testability

Never optimize architecture for cleverness.

Prefer simple systems.

Objectives

Produce the complete technical blueprint for the project.

The architecture should allow an engineer to implement HospitalityAI without making architectural decisions later.

Required Deliverables

Create

docs/architecture/

README.md

01-system-overview.md

02-context-diagram.md

03-container-diagram.md

04-component-diagram.md

05-domain-boundaries.md

06-request-flow.md

07-ai-architecture.md

08-agent-architecture.md

09-rag-architecture.md

10-ml-architecture.md

11-data-architecture.md

12-deployment-architecture.md

13-security-architecture.md

14-observability-architecture.md

15-technology-decisions.md

Every document must explain why decisions were made, not only what was chosen.

docs/architecture/

↓

.specs/backend/

↓

.specs/database/

↓

.specs/agents/

↓

.specs/ai/

High-Level System

HospitalityAI consists of multiple logical platforms.

                 Guest

                   │

            Frontend UI

                   │

             FastAPI Gateway

                   │

 ───────────────────────────────────

      Business Platform

      AI Platform

      Data Platform

      ML Platform

      Knowledge Platform

 ───────────────────────────────────

 PostgreSQL

 Redis

 Qdrant

 Object Storage
Major Platforms

The architecture shall define the following platforms.

API Platform

Responsibilities

authentication
routing
validation
authorization
API versioning

No business logic.

Business Platform

Contains

Reservation

Guest

Restaurant

Spa

Reviews

Operations

Revenue

Every business module must be isolated.

AI Platform

Contains

Prompt Manager

LLM Provider

Tool Registry

Memory Manager

Model Router

Evaluation

Provider adapters

The AI platform must never depend on one model provider.

Agent Platform

Contains

Planner

Executor

Supervisor

Router

Workflow Engine

Tool Calling

Every agent is independent.

Knowledge Platform

Contains

Document Processing

Chunking

Embedding

Vector Storage

Retrieval

Reranking

Citation

Knowledge Evaluation

ML Platform

Contains

Training

Inference

Evaluation

Feature Engineering

Experiment Tracking

Model Registry

Monitoring

Data Platform

Contains

ETL

Validation

Cleaning

Transformation

Feature Store

Metadata

Versioning

Dashboard Platform

Contains

Analytics

Business KPIs

Forecasts

Operational Metrics

Agent Metrics

ML Metrics

Architecture Principles

Every service

Must

Single responsibility

Own its own domain

Hide implementation

Expose clean interfaces

Be independently testable

Must Never

Access another service's database directly

Duplicate logic

Contain UI code

Dependency Rules

Allowed

Frontend

↓

API

↓

Application

↓

Domain

↓

Infrastructure

Forbidden

Infrastructure

↓

Application

Business rules must never depend on infrastructure.

Communication

Internal communication

REST

Future

Message queues

No synchronous dependency chains longer than three services.

Data Flow

Every request

Client

↓

API

↓

Application Service

↓

Domain

↓

Repository

↓

Database

Never

Client

↓

Database
AI Flow

Every AI request

Prompt

↓

Router

↓

Planner

↓

Tools

↓

Memory

↓

Retriever

↓

LLM

↓

Validator

↓

Response

The LLM must never be called directly from business modules.

RAG Flow
Documents

↓

Parser

↓

Cleaner

↓

Chunker

↓

Embedding

↓

Qdrant

↓

Retriever

↓

Reranker

↓

Prompt

↓

LLM
Machine Learning Flow
Raw Data

↓

Validation

↓

Cleaning

↓

Feature Engineering

↓

Training

↓

Evaluation

↓

MLflow

↓

Registry

↓

Inference
Deployment Architecture

Architecture should support

Development

Testing

Production

All services containerized.

Every component deployable independently.

Security Architecture

Define

Authentication

Authorization

Secrets

Encryption

Audit Logs

Input Validation

Rate Limiting

Threat Model

Observability

Every service

Must expose

Metrics

Health

Structured Logs

Tracing

Technology Decisions

Every technology selection must include

Reason

Alternatives Considered

Trade-offs

Future Migration Strategy

Example

Instead of

"Use PostgreSQL"

Document

Why PostgreSQL

Why not MongoDB

Why relational fits reservations

Migration path if scaling changes

Architecture Decision Records

Every significant architectural decision requires an ADR.

Examples

Use LangGraph

Use PostgreSQL

Use FastAPI

Use Docker

Use Qdrant

Use MLflow

Use Redis

Every ADR must explain

Context

Decision

Consequences

Alternatives

RFCs

Architecture loop should automatically generate RFC placeholders for

Backend

Agents

RAG

ML

Dashboard

Deployment

Authentication

ETL

Quality Gates

Loop 02 is complete only if

Every architecture document exists.
Every platform boundary is documented.
Every dependency direction is defined.
Every major technology has an ADR.
Every architectural decision has a rationale.
No implementation details appear in architecture documents.
The architecture supports all functional requirements from Loop 01.
Exit Criteria

The architecture should be detailed enough that implementation teams can begin development without making additional structural decisions.

Implementation should become an execution exercise rather than an architecture exercise.

Deliverables

At the end of Loop 02, the repository should contain:

docs/architecture/
    README.md
    01-system-overview.md
    02-context-diagram.md
    03-container-diagram.md
    04-component-diagram.md
    05-domain-boundaries.md
    06-request-flow.md
    07-ai-architecture.md
    08-agent-architecture.md
    09-rag-architecture.md
    10-ml-architecture.md
    11-data-architecture.md
    12-deployment-architecture.md
    13-security-architecture.md
    14-observability-architecture.md
    15-technology-decisions.md

.adr/
    ADR-0001-fastapi.md
    ADR-0002-postgresql.md
    ADR-0003-qdrant.md
    ADR-0004-langgraph.md
    ADR-0005-redis.md
    ADR-0006-mlflow.md

.rfc/
    RFC-0001-backend.md
    RFC-0002-ai-platform.md
    RFC-0003-rag.md
    RFC-0004-ml-platform.md
    RFC-0005-dashboard.md