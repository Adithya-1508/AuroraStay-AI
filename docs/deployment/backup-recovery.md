# Database Backup & Recovery

This document specifies the backup frequency, retention targets, and recovery operations.

## 1. Automated Backup Workflows

Automated CronJobs execute daily backups:
- **PostgreSQL Database**:
  - Script: `deployment/backups/db_backup.sh`
  - Output: `db_backup_[TIMESTAMP].sql`
  - Destination: OCI Object Storage bucket.
- **Qdrant Vector Database**:
  - Script: `deployment/backups/qdrant_backup.sh`
  - Output: Collection snapshot files.

## 2. Restore Procedures

If data corruption occurs, recovery is initiated using the restore scripts:
1. **Restore PostgreSQL Database**:
   ```bash
   ./deployment/restore/db_restore.sh /path/to/db_backup.sql
   ```
2. **Restore Qdrant Collections**:
   ```bash
   ./deployment/restore/qdrant_restore.sh /path/to/snapshot.snapshot
   ```
These operations clear existing corrupted collections/tables and rebuild the active state.
