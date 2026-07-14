# Least Privilege Authorization Engine

This module resolves scopes and resource permissions based on user roles and profiles.

## Scope Definitions

| Resource Namespace | Permitted Operation | Scopes Required |
|---|---|---|
| Reservations | View reservations history | `reservation:read` |
| Reservations | Add or modify bookings | `reservation:write` |
| Guests | View customer profiles | `guest:read` |
| Guests | Purge PII under GDPR | `guest:delete` |
| Revenue | Read pricing charts | `revenue:read` |
| Revenue | Set rates, discounts | `revenue:write` |
| System Audit | Query security audits | `audit:read` |
| Console | Toggle maintenance states | `console:write` |

## Enforcement Flow

1. **Extraction**: Decode JWT token and retrieve the user's mapped roles list.
2. **Expansion**: Resolve roles into set of associated granular permissions.
3. **Assertion**: Verify that the required action scope matches one of the user's allowed permissions.
