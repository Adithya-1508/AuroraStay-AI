# Security Architecture

Security is integrated natively in the logical layers of HospitalityAI.

## 1. Authentication Flow (JWT)

```
   Guest / Staff ──> POST /api/v1/auth/login ──> Returns RS256 JWT Token
   Private Route <──   Provide JWT Header     <── Appended to requests
```

1. Secure routes validate incoming HTTP `Authorization` headers.
2. Tokens must match the project's RS256 algorithm public key.
3. Expired tokens (default lifetime: 1 hour) are immediately rejected with `401 Unauthorized` responses.

---

## 2. Role-Based Access Control (RBAC) Matrix

| Route Endpoint | Guest | Staff | Manager | Admin |
| --- | :---: | :---: | :---: | :---: |
| `GET /api/v1/concierge/chat` | ✓ | ✓ | ✓ | ✓ |
| `GET /api/v1/reservations/me` | ✓ | ✓ | ✓ | ✓ |
| `POST /api/v1/reservations/` | ✓ | ✓ | ✓ | ✓ |
| `PUT /api/v1/reservations/{id}` | (Own Only) | ✓ | ✓ | ✓ |
| `GET /api/v1/housekeeping/tasks` | ✗ | ✓ | ✓ | ✓ |
| `POST /api/v1/housekeeping/tasks` | ✗ | ✓ | ✓ | ✓ |
| `GET /api/v1/analytics/revenue` | ✗ | ✗ | ✓ | ✓ |
| `POST /api/v1/ml/retrain` | ✗ | ✗ | ✗ | ✓ |
| `GET /api/v1/admin/audit-logs` | ✗ | ✗ | ✗ | ✓ |

---

## 3. Data Protection Guidelines

- **Transit Protection**: Enforce TLS 1.3 for all HTTP REST traffic, disabling outdated protocol parameters (SSLv3, TLS 1.0).
- **At-Rest Protection**: Database backups must be encrypted. Sensitive guest profile columns (names, phone numbers) are masked in standard database logs.
- **Input Sanitization**:
  - API payloads are parsed through strict Pydantic schemas.
  - SQL inputs are mapped using SQLAlchemy ORM variables, preventing SQL injections.
  - LLM inputs are scrubbed of HTML tags and text injections before prompt compilation.
