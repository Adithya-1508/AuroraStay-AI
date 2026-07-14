# Immutable Audit Logging

This module implements a tamper-evident audit trail utilizing a cryptographic block hash chain.

## Hash Chain Design

Each log entry is bound to the preceding entry hash value, forming an immutable sequence:

```
+--------------------------------------------------------+
| Entry 1                                                |
| timestamp | identity_id | action | status | prev_hash: | <---+ (Initial hash "0000...")
| Hash = SHA-256(Payload)                                |
+--------------------------------------------------------+
                            |
                            v
+--------------------------------------------------------+
| Entry 2                                                |
| timestamp | identity_id | action | status | prev_hash: | <---+ (Entry 1 Hash)
| Hash = SHA-256(Payload)                                |
+--------------------------------------------------------+
                            |
                            v
+--------------------------------------------------------+
| Entry 3                                                |
| timestamp | identity_id | action | status | prev_hash: | <---+ (Entry 2 Hash)
| Hash = SHA-256(Payload)                                |
+--------------------------------------------------------+
```

## Verification Routine

- **traversal**: Reads through all log blocks sequentially.
- **Assertion**:
  - Validates that `previous_hash` matches the hash computed for the preceding entry.
  - Recomputes the SHA-256 of the payload and asserts it matches the record's stored `hash`.
- **Alerting**: Failure in verification immediately triggers critical security alerts and locks down the administration panel.
