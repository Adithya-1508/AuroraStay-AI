# Authentication Services

This module handles session establishment, validation, and programmatic key verification.

## 1. JSON Web Tokens (JWT)

- **Algorithm**: HS256 (HMAC SHA-256)
- **Token Types**:
  - **Access Tokens**: Expire in 15 minutes, containing identity, type, roles, and department.
  - **Refresh Tokens**: Expire in 7 days, containing subject reference for token renewal.
- **Revocation**: Blacklists active JWT access signatures inside a transient revoked memory set upon explicit user logouts.

## 2. API Keys Manager

- **Format**: Prefixed tokens starting with `hk_` followed by cryptographically secure random bytes.
- **Hashing**: Stores only SHA-256 hashed values of keys in the database.
- **Validation**: Verifies client header tokens against active hashes to identify corresponding agents and permissions.
