# Spec: Middleware Pipeline

- **Status**: Ready
- **Owner**: Backend Framework Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Specifies the global middleware stack executed on every HTTP request/response cycle.

## 2. Middleware Sequence
Requests pass through middleware layers in the following order:
1. **Security Headers & CORS**: Injects basic headers (HSTS, CSP, Frame Options) and permits verified origin endpoints.
2. **Correlation ID**: Inspects incoming requests for `X-Request-ID`. If missing, generates a unique UUID. Attaches it to the request context.
3. **Request Timing**: Measures elapsed execution duration. Injects `X-Response-Time` header on output.
4. **Structured Request Logging**: Captures request metadata (method, route path, user-agent) and response metadata (status code, latency, request_id) and routes to structlog.

## 3. Correlation ID Rules
- Incoming header check: `X-Request-ID`
- Fallback: Generate `f"req_{uuid.uuid4()}"`
- Response header injected: `X-Request-ID`
- Context storage: Injected into FastAPI's `request.state.request_id` for logger access.
