#!/bin/bash
set -e

# Configuration
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"5432"}
DB_USER=${DB_USER:-"postgres"}
DB_NAME=${DB_NAME:-"hospitality"}
BACKUP_DIR=${BACKUP_DIR:-"/tmp/backups"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql"

mkdir -p "${BACKUP_DIR}"

echo "Starting PostgreSQL logical database backup..."
PGPASSWORD="${DB_PASSWORD}" pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -F c -b -v -f "${BACKUP_FILE}"
echo "Backup successfully completed: ${BACKUP_FILE}"

# Optional: upload to object storage bucket
if [ -n "${OCI_BUCKET_NAME}" ]; then
  echo "Uploading backup to OCI Object Storage bucket: ${OCI_BUCKET_NAME}..."
  oci os object put --bucket-name "${OCI_BUCKET_NAME}" --file "${BACKUP_FILE}" --name "db_backups/db_backup_${TIMESTAMP}.sql"
  echo "Upload complete."
fi
