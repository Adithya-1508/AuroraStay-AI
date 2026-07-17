# Runbook: Security Incident Triage & Response

This runbook guides administrators through containment steps upon receiving security alert notifications.

## 1. Triage Actions

1. **Check Incident Tracker**:
   Query active logged incidents:
   ```bash
   curl -s http://hospitalityai.local/api/v1/security/incidents
   ```
2. **Review Risk Levels**:
   Query active client risk evaluation:
   ```bash
   curl -s http://hospitalityai.local/api/v1/security/risk
   ```

## 2. Containment Protocols

1. **Bypass / Suspend Compromised Keys**:
   If an API key is leaking or compromised:
   - Identify the user/agent ID associated with the key.
   - Set key status to INACTIVE.
2. **Lock Suspected Accounts**:
   Suspend the user profile inside the database:
   ```bash
   curl -X PUT http://hospitalityai.local/api/v1/users/[USER_ID] -d '{"status": "SUSPENDED"}'
   ```
3. **Toggle Maintenance Mode**:
   For critical compromises (e.g. data breach or prompt injection sweeps), lock down the API gateway:
   - Toggle maintenance mode to True in the admin console.
   - This blocks all modifications across endpoints.
