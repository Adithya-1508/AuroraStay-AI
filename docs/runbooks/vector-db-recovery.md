# Runbook: Qdrant Vector Collection Recovery

This runbook guides administrators through restoring Qdrant vector collections from snapshots.

## 1. Prerequisites

- Curl CLI tool.
- Access to the target Qdrant API service endpoint (default: Port 6333).

## 2. Restore Steps

1. **Verify Snapshot File**:
   Ensure collection snapshot file exists.
2. **Execute Restoration**:
   ```bash
   ./deployment/restore/qdrant_restore.sh /path/to/snapshot.snapshot
   ```
3. **Verify Restoration**:
   Query the collection metrics endpoint to check the vector counts:
   ```bash
   curl -s http://localhost:6333/collections/hospitality_knowledge
   ```
   Confirm vector counts match expected indexes.
