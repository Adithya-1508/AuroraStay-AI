# API Directory

## Purpose
The Presentation Layer. Exposes the FastAPI REST routers, endpoint routing, API payload serialization/deserialization models, and rate limiters. Crucially, **no business logic is allowed in this directory**. Routes should only validate incoming payloads and delegate executions to the Application Services inside the `business/` layer.

## Ownership
- **Owner**: Backend Platform Team (Antigravity AI Coding Agent)
- **Primary Domain**: REST Interfaces, CORS, OpenAPI schemas, Rate Limiting

## Key Responsibilities
1. HTTP entry points and route mapping.
2. Request and response Pydantic schema validation.
3. User authorization checks and security middleware.
