# Spec: API Structure and Response Schemas

- **Status**: Ready
- **Owner**: Backend Framework Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines the routing prefix standards, versioning guidelines, and standard response wraps for all APIs.

## 2. API Prefix and Versioning
- All endpoints must be versioned. The default version prefix is `/api/v1/`.
- No endpoints should exist outside the versioned router namespace (except health and documentation routes).

## 3. Success Response Wrapper (JSON)
All successful endpoints must return status code `200` (or `201` for creation) with the following structure:
```json
{
  "success": true,
  "data": {},
  "metadata": {},
  "request_id": "req_uuid_string",
  "timestamp": "ISO-8601-format-timestamp"
}
```

## 4. Error Response Wrapper (JSON)
All exceptions caught by the handler framework must return appropriate HTTP status codes (e.g. `400`, `401`, `403`, `404`, `500`) with the following structure:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human-readable error details"
  },
  "request_id": "req_uuid_string",
  "timestamp": "ISO-8601-format-timestamp"
}
```

## 5. OpenAPI Customizations
- The OpenAPI generator must expose custom metadata (Title: "HospitalityAI API", Description, Version).
- Enforce custom schema generation for Pydantic models.
- Register JWT Bearer Security schemas in the generated JSON.
