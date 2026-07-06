# Spec: Security, Authentication, and RBAC

- **Status**: Ready
- **Owner**: Security Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines the cryptography standards, JWT token layouts, and role verification controls.

## 2. JWT Configuration
- **Algorithm**: `HS256` (HMAC SHA-256)
- **Secret Key**: Loaded via Settings.
- **Expiration Thresholds**:
  - Access Token: 15 minutes.
  - Refresh Token: 7 days.
- **Claims Schema**:
  ```json
  {
    "sub": "usr_uuid_string",
    "role": "Guest | Staff | Manager | Administrator | AIService | Worker",
    "exp": 1720000000,
    "iat": 1719999000
  }
  ```

## 3. Password Hashing
- Implement password hashing using `bcrypt` (or cryptography equivalents) to generate secure salts.
- Do not store raw passwords.

## 4. Role-Based Access Control (RBAC)
FastAPI dependencies are declared to assert roles:
- `require_role(allowed_roles: List[str])`: Yields current user payload if verified, else raises `AuthenticationError` / `403 Forbidden`.
