# Security, Identity & Enterprise Administration Console

This directory contains system documentation for the security and identity platform integrated in the Hospitality AI ecosystem.

## Platform Architecture Diagram

```mermaid
graph TD
    Client[REST API Client] -->|HTTPS Requests| RateLimiter[Sliding Window Rate Limiter]
    RateLimiter -->|Passed Check| API_Router[FastAPI V1 Routes]
    
    API_Router -->|Validate Token| JWTAuth[JWT Authentication Service]
    API_Router -->|Validate Key| APIKeyMgr[API Key Registry Manager]
    
    JWTAuth -->|Extract Roles| PermissionEngine[Least Privilege Authorization Engine]
    APIKeyMgr -->|Check Scopes| PermissionEngine
    
    PermissionEngine -->|Verify Policy| ABACPolicy[Attribute-Based Control Engine]
    ABACPolicy -->|Filter Context| AccessGranted[Access Granted to Business Logic]
    
    AccessGranted -->|Input Scanner| Guardrails[AI Input/Output Guardrails]
    AccessGranted -->|Encrypt PII| EncryptionSvc[AES Encryption Service]
    AccessGranted -->|Retrieve Keys| SecretsManager[Environment Secrets Manager]
    
    Operations[Privileged Actions] -->|Log Event| AuditTrail[Cryptographic Hash Audit Trail]
    AuditTrail -->|Alert Incidents| IncidentTracker[Security Incident Tracker]
    
    AdminConsole[Enterprise Administration Console] -->|Control States| API_Router
```

## Security Documentation Modules

Select a specific documentation module below for detailed design, guidelines, and APIs:

1. **[Identity & Directory Services](identity.md)**: Standard models for user accounts, API key configurations, and system identities.
2. **[Authentication Services](authentication.md)**: Stateful JWT lifecycle manager, API keys hashing validation registry, and token revocation lists.
3. **[Least Privilege Authorization Engine](authorization.md)**: Direct scope validations, endpoint permissions, and RBAC privilege mappings.
4. **[Attribute-Based Access Control (ABAC)](rbac.md)**: Operational shift hours windows, IP address blacklists, and department isolation controls.
5. **[AI Guardrails & Secrets Protection](ai-security.md)**: Prompt injection/leakage scanners, logging masks, and sliding window API rate limits.
6. **[GDPR Purge & Data Privacy Compliance](compliance.md)**: PII anonymizers, right-to-be-forgotten hooks, and AES field-level encryption.
7. **[Immutable Audit Logging](audit.md)**: Cryptographically chained block verification log entries.
8. **[Enterprise Console & AI Governance](administration.md)**: Model version gate approvals, prompt templates registrations, and maintenance toggles.
9. **[Security Incident Tracker](incident-response.md)**: Incident isolation workflows and containments response metrics.
