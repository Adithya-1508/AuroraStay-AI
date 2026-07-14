# Security Incident Tracker

This module logs, tracks, and manages security incident tickets and risk scoring.

## Risk Assessment Metrics

The evaluator computes active risk metrics based on client requests:
- **Failed Logins**: Adds `0.15` per failed attempt.
- **Unauthorized Actions**: Adds `0.10` per scope violation.
- **Prompt Injection**: Adds `0.70` immediately to trigger a `"CRITICAL"` risk level.

## Containment Status Workflow

```
+-----------+       +---------------+       +---------------+
|   OPEN    |  -->  |   CONTAINED   |  -->  |   RESOLVED    |
+-----------+       +---------------+       +---------------+
```

1. **OPEN**: Incident detected and ticket created (e.g., Compromised API Key, Prompt Injection).
2. **CONTAINED**: Active mitigation applied (e.g., API key suspended, user profile locked).
3. **RESOLVED**: Security audits verified, root cause addressed, and ticket closed.
