# Attribute-Based & Role-Based Access Control

This module combines Role-Based Access Control (RBAC) with dynamic context checks via Attribute-Based Access Control (ABAC).

## Role-Based Mapping (RBAC)

Enterprise roles have direct mappings to granular permissions:
- **Guest**: `reservation:read`
- **Receptionist**: `reservation:read`, `reservation:write`, `guest:read`
- **Revenue Manager**: `revenue:read`, `revenue:write`
- **System Auditor**: `audit:read`
- **Administrator**: All permissions including user administration and console writes.

## Attribute-Based Evaluation (ABAC)

Dynamic rules are evaluated at request time based on the active client context:
1. **IP Range Restrictions**: Rejects requests originating from blacklisted IPs (e.g., `192.168.1.99`).
2. **Operational Shift Windows**: resticts access for operational staff (`Reception`, `Housekeeping`, `Maintenance`) to standard shift windows (`06:00:00` to `22:00:00`). Managers and Administrators bypass this check.
3. **Department Isolation**: Users are blocked from accessing resources belonging to other departments, unless the user belongs to `ALL` or `Administration` (least-privilege isolation).
