# AI Governance Manual

## Overview
AI Governance registers approved configurations, specifies ownership, and guarantees compliance with local PII privacy constraints.

## PII Redaction Masks
Prompt variables are processed through regular expression filters. Any indicators matching the patterns below are replaced automatically:
- **Emails**: Redacted to `[REDACTED_EMAIL]`.
- **Phone Numbers**: Redacted to `[REDACTED_PHONE]`.

## Assets Registry
Approved models, prompts, and agents are registered with respective team owners (e.g. Revenue Team, Guest Experience Team) and risk levels (LOW, MEDIUM, HIGH).

## REST API
- **GET** `/api/v1/observability/models`: Lists registered governance models and ownership details.
