# Security Principles

Security is integrated by default in HospitalityAI. Every design and implementation must enforce these guidelines.

## 1. Input Validation & Sanitization
- Never trust user input.
- Validate all API payloads using Pydantic schemas.
- Sanitize data before persistence or presentation to prevent injection attacks.

## 2. Authentication & Authorization
- **JWT Authentication**: All secure endpoints must require valid JSON Web Tokens (JWT) for authentication.
- **Role-Based Access Control (RBAC)**: Enforce access control at the service layer based on user roles (e.g. Guest, Staff, Manager, Admin).

## 3. Secrets Management
- Never hardcode credentials, API keys, certificates, or tokens.
- Load configurations and secrets exclusively from environment variables or a secure vault.
- Exclude settings files containing secrets from version control (using `.gitignore`).

## 4. SQL Injection Prevention
- Use SQLAlchemy ORM parameter binding for all database queries.
- Avoid writing raw SQL queries. If raw SQL is required, use parameterized queries.

## 5. Security Logging
- Log security-critical events: login attempts, access failures, password/key rotations, and administrator configuration changes.
- **Never log sensitive data** such as raw passwords, keys, or credit card numbers.

## 6. Rate Limiting
- Public API routes must have rate limits to protect against Denial of Service (DoS) and brute force attacks.
