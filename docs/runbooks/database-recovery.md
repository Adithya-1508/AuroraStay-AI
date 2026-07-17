# Runbook: PostgreSQL Database Restoration

This runbook guides administrators through restoring database tables from backup logical dumps.

## 1. Prerequisites

- Installed PostgreSQL client tools (`pg_restore`).
- Target DB access credentials.

## 2. Restore Steps

1. **Verify Backup File Integrity**:
   Confirm backup exists in the target directory or OCI object bucket.
2. **Execute Restoration**:
   ```bash
   ./deployment/restore/db_restore.sh /path/to/db_backup.sql
   ```
3. **Verify Restoration Success**:
   Connect to the database and query the table row counts:
   ```sql
   SELECT count(*) FROM reservations;
   ```
   Confirm row counts match the backup records.
4. **Trigger Service Rollout**:
   Restart backend pods to clean cache variables:
   ```bash
   kubectl rollout restart deployment/backend-api -n hospitality
   ```
