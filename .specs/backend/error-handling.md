# Spec: Global Exception Handling

- **Status**: Ready
- **Owner**: Backend Framework Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define how exceptions are caught, logged, and mapped to HTTP status codes.

## 2. HTTP Error Mappings

| Raised Exception Class | HTTP Status Code | Response Code | Description |
| --- | --- | --- | --- |
| **ValidationError** (Pydantic) | `422 Unprocessable Entity` | `VALIDATION_ERROR` | Schema validation fails. |
| **AuthenticationError** | `401 Unauthorized` | `UNAUTHENTICATED` | Token is invalid or missing. |
| **PermissionError** / Forbidden | `403 Forbidden` | `UNAUTHORIZED` | Role lacks permissions. |
| **EntityNotFoundError** | `404 Not Found` | `NOT_FOUND` | Database lookup returns empty. |
| **BusinessRuleError** | `400 Bad Request` | `BUSINESS_VIOLATION` | Aggregate invariants checks fail. |
| **Exception** (Catch-All) | `500 Internal Server Error` | `INTERNAL_SERVER_ERROR` | Unknown system failure. |

## 3. Log Details
For all `500` status errors, the handler must log the full exception stack trace to structlog. For client-side `4xx` errors, log messages are registered as warnings, without stack traces.
