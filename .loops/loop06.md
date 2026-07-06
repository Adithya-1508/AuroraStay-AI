LOOP 06 — Data Platform & Persistence Layer

Version: 1.0

Project: HospitalityAI

Status: Mandatory

Prerequisites

Loop 00 — Constitution
Loop 01 — Product Requirements
Loop 02 — Architecture
Loop 03 — Domain Modeling
Loop 04 — Repository Bootstrap
Loop 05 — Backend Core Platform
Purpose

Build HospitalityAI's enterprise-grade data platform.

This loop is responsible for:

Database architecture
Persistence
Repository implementations
ETL framework
Data validation
Feature Store foundation
Data Quality framework

No AI or Machine Learning should exist after this loop.

This is purely the data layer.

Philosophy

Data is a product.

Every dataset should be:

versioned
validated
documented
observable
reproducible
Objectives

Build a production-ready persistence platform capable of supporting

Reservations
Guests
Reviews
AI
ML
Analytics

without requiring future architectural changes.

Deliverables

Create

backend/

repositories/
    base/
    postgres/

models/
    guest.py
    reservation.py
    room.py
    review.py
    employee.py
    conversation.py
    recommendation.py
    forecast.py
    knowledge_document.py

database/
    session.py
    engine.py
    migrations/
    seed/
    factories/

etl/
    extract/
    transform/
    load/
    validation/
    metadata/

feature_store/

data_quality/

schemas/

Database Design

Use

PostgreSQL

ORM

SQLAlchemy 2.x

Migration

Alembic

No raw SQL unless justified by an ADR.

Entity Models

Implement

Guest

Reservation

Room

RoomType

Review

Restaurant

Spa

Conversation

KnowledgeDocument

Forecast

Recommendation

Notification

Employee

Every model must include

UUID primary key
timestamps
soft delete
audit metadata
optimistic locking (version field where appropriate)
Relationships

Examples

Guest

↓

Reservations

↓

Room

↓

Reviews

KnowledgeDocument

↓

Embeddings (logical relationship)

↓

Retriever

Relationships must be explicit and documented.

Repository Layer

Implement concrete repositories

GuestRepository

ReservationRepository

ReviewRepository

KnowledgeRepository

ForecastRepository

RecommendationRepository

Every repository must support

Create

Update

Delete (soft delete)

Get by ID

Search

Pagination

Filtering

Sorting

Repositories must not contain business logic.

Unit of Work

Implement a Unit of Work pattern to manage transactions.

Services must not manually commit database transactions.

Support

Commit
Rollback
Nested transaction handling
ETL Platform

Create an ETL framework with three stages:

Extract
    ↓
Transform
    ↓
Load

Organize extractors for:

CSV files
JSON
REST APIs
Mock hotel systems

Transformers should handle:

Cleaning
Normalization
Validation
Deduplication
Feature engineering hooks

Loaders should support:

PostgreSQL
Future data warehouse integration
Data Validation

Implement validation framework

Checks

Nulls

Duplicates

Schema validation

Referential integrity

Date consistency

Business constraints

Validation failures should generate reports instead of silently failing.

Feature Store Foundation

Create

feature_store/

registry/

pipelines/

transformations/

metadata/

The Feature Store should

Track

Feature ownership

Feature version

Description

Dependencies

Source dataset

Refresh frequency

Actual ML features will be created later.

Data Quality

Implement quality framework

Metrics

Completeness

Accuracy

Consistency

Uniqueness

Timeliness

Validity

Generate quality reports after ETL execution.

Database Seeding

Create realistic demo data

Guests

Rooms

Reservations

Reviews

Restaurants

Spa bookings

Employees

No fake placeholder values like

John Doe

Test User

Sample Data

Generate believable hotel data.

Indexing Strategy

Design indexes for

Reservation lookup

Guest search

Room availability

Review queries

Conversation history

Document retrieval

Document why each index exists.

Data Versioning

Every ETL execution should record

Dataset version

Source

Timestamp

Row counts

Validation status

Execution duration

Metadata Catalog

Create metadata registry

For every dataset record

Name

Owner

Description

Schema

Refresh schedule

Quality score

Testing

Tests required for

Repositories

Transactions

ETL

Validation

Migrations

Data Quality

Seed scripts

Coverage target

≥95%

Documentation

Generate

docs/data/

database-schema.md

entity-relationships.md

repository-pattern.md

etl-pipeline.md

feature-store.md

data-quality.md

migrations.md

metadata-catalog.md
Quality Gates

Loop fails if

❌ AI agents are implemented

❌ LangGraph exists

❌ LLM calls exist

❌ FastAPI business endpoints exist

❌ Machine Learning models exist

Those belong to future loops.

Acceptance Criteria

The platform should

Connect to PostgreSQL
Apply Alembic migrations
Seed demo data
Perform CRUD through repositories
Execute ETL jobs
Validate datasets
Produce metadata
Generate quality reports
Support transactional integrity
Pass all tests
Definition of Done

Loop 06 is complete only if

Database schema implemented.
Repository layer complete.
Transaction management operational.
ETL framework functional.
Data validation framework operational.
Feature Store foundation exists.
Metadata catalog implemented.
Documentation complete.
Tests passing.
Exit Criteria

At the end of Loop 06, HospitalityAI possesses a production-ready data platform capable of serving every future subsystem.

The backend can now persist, query, validate, and transform hotel data without any AI or business-specific implementation.

Engineering Note for Antigravity

Before implementation:

Review the domain model from Loop 03.
Generate an ER diagram from the domain entities.
Create Alembic migration plans before writing models.
Implement repositories before services.
Validate all migrations against an empty database.
Seed realistic hospitality data for local development.
Ensure every repository method has corresponding unit tests.
Verify that no AI, ML, or business workflow code leaks into the data layer.

Should generate

.specs/database/

guest.md

reservation.md

room.md

review.md

employee.md

forecast.md

recommendation.md

And

.specs/etl/

extract.md

transform.md

load.md

validation.md