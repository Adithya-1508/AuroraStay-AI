LOOP 04 — Repository Bootstrap & Engineering Infrastructure

Version: 1.0

Project: HospitalityAI

Status: Mandatory

Prerequisites:

Loop 00 completed
Loop 01 completed
Loop 02 completed
Loop 03 completed
Purpose

Build the engineering foundation of HospitalityAI.

This loop does not implement business features.

Instead, it establishes a production-grade engineering environment so that every future loop can focus solely on feature development.

The repository should become immediately usable by any engineer or coding agent after this loop.

Objectives

By the end of this loop, HospitalityAI should have:

Complete repository structure
Development environment
Docker infrastructure
Dependency management
Code quality tools
GitHub Actions
Local development workflow
Testing framework
Documentation skeleton
Configuration management
Deliverables

Create the following structure:

HospitalityAI/

.foundation/
.loops/
.templates/
.adr/
.rfc/
.prd/

docs/
architecture/
domain/
api/
deployment/

apps/

backend/

frontend/

dashboard/

services/

agents/

ml/

etl/

workers/

knowledge/

shared/

config/

scripts/

docker/

tests/

.github/

.env.example

.gitignore

README.md

LICENSE

Makefile

docker-compose.yml

pyproject.toml

pre-commit-config.yaml
Python Environment

Use

Python 3.12+

Package Manager

uv

Dependency groups

base

dev

test

docs

ml

ai

Never install unnecessary packages.

Dependencies must remain minimal.

Development Standards

Configure

Black

Ruff

mypy

pytest

pre-commit

Coverage

isort

Every configuration should live inside

pyproject.toml
Docker

Create

docker/

backend.Dockerfile

frontend.Dockerfile

worker.Dockerfile

dashboard.Dockerfile

Root

docker-compose.yml

Must support

Backend

PostgreSQL

Redis

Qdrant

MLflow

Prometheus

Grafana

All services should be networked correctly.

Health checks are mandatory.

Environment Configuration

Create

.env.example

Containing

DATABASE_URL

REDIS_URL

QDRANT_URL

JWT_SECRET

MODEL_PROVIDER

NVIDIA_API_KEY

OLLAMA_URL

MLFLOW_URI

LOG_LEVEL

Never commit

.env
Repository Rules

Every directory must contain

README.md

Explaining

Purpose

Responsibilities

Allowed Dependencies

Examples

Git

Configure

.gitignore

Include

Python

Docker

IDE

OS

Secrets

ML Artifacts

Coverage

Logs

GitHub

Create

.github/

workflows/

ISSUE_TEMPLATE/

PULL_REQUEST_TEMPLATE.md

CODEOWNERS
CI Pipeline

Create GitHub Actions

Run

Install

↓

Lint

↓

Format Check

↓

Type Check

↓

Tests

↓

Coverage

↓

Docker Build

Pull requests cannot merge if any stage fails.

Makefile

Create commands

make setup

make lint

make format

make test

make typecheck

make docker

make run

make clean

make docs

make coverage
Scripts

Create

scripts/

bootstrap.py

healthcheck.py

seed_data.py

reset_db.py

lint_all.py
Logging

Configure

Structured JSON logging.

Every future service must inherit from the shared logging configuration.

Shared Package

Create

shared/

config/

exceptions/

logging/

utils/

types/

constants/

No business logic.

Only reusable infrastructure.

Configuration System

Use

Pydantic Settings

Environment variables

Configuration must support

Development

Testing

Production

Testing Infrastructure

Configure

pytest

coverage

Fixtures

Factories

Test utilities

Mock providers

Folder

tests/

unit/

integration/

e2e/

fixtures/

factories/

utils/
Documentation

Generate

Root README

Contributing Guide

Development Guide

Repository Structure

Local Setup

Coding Standards

Local Development

One command should start everything.

Example

make setup

make run

or

docker compose up

No manual setup should be required.

Dependency Rules

Every module

Must

Declare dependencies explicitly.

Avoid circular imports.

Infrastructure packages cannot depend on business modules.

Acceptance Criteria

The repository should:

Clone successfully.
Install with one command.
Start with one command.
Run tests.
Pass linting.
Pass type checking.
Build Docker images.
Generate documentation.
Support local development.
Be understandable by a new contributor within 15 minutes.
Quality Gates

Before completion

Docker Compose builds successfully.
GitHub Actions passes.
Ruff passes.
Black passes.
mypy passes.
pytest passes.
Coverage reporting configured.
Pre-commit hooks installed.
README complete.
No placeholder implementations.
Definition of Done

Loop 04 is complete only if:

Repository structure exists.
Development tooling is operational.
CI/CD is configured.
Docker environment is functional.
Testing framework is ready.
Documentation skeleton exists.
Environment configuration is complete.
Local onboarding requires no manual intervention beyond documented setup.
Exit Criteria

At the end of Loop 04:

The repository is fully bootstrapped.
Any engineer can clone it and begin implementing features immediately.
Future loops (Backend, Data Platform, AI Platform, etc.) should only add business functionality, not revisit tooling or repository setup.
Deliverables
README.md
LICENSE
Makefile
docker-compose.yml
pyproject.toml
pre-commit-config.yaml
.env.example

.github/
docker/
scripts/
shared/
config/
tests/

All directory READMEs

Working CI pipeline

Working Docker environment

Working local development environment

Repository bootstrap should create -> If the folders are already there, create ones that are not there.

.specs/

README.md

backend/

database/

api/

agents/

ai/

etl/

ml/

dashboard/

testing/

deployment/

security/ 
