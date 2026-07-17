#!/bin/bash
set -e

QDRANT_URL=${QDRANT_URL:-"http://localhost:6333"}
COLLECTION_NAME=${COLLECTION_NAME:-"hospitality_knowledge"}
BACKUP_DIR=${BACKUP_DIR:-"/tmp/backups"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "${BACKUP_DIR}"

echo "Triggering Qdrant collection snapshot for collection: ${COLLECTION_NAME}..."
SNAPSHOT_RESPONSE=$(curl -s -X POST "${QDRANT_URL}/collections/${COLLECTION_NAME}/snapshots")
SNAPSHOT_NAME=$(echo "${SNAPSHOT_RESPONSE}" | grep -o '"name":"[^"]*' | grep -o '[^"]*$')

if [ -z "${SNAPSHOT_NAME}" ]; then
  echo "Error triggering snapshot. Response: ${SNAPSHOT_RESPONSE}"
  exit 1
fi

echo "Downloading snapshot: ${SNAPSHOT_NAME}..."
curl -s -o "${BACKUP_DIR}/${SNAPSHOT_NAME}" "${QDRANT_URL}/collections/${COLLECTION_NAME}/snapshots/${SNAPSHOT_NAME}"
echo "Vector DB collection backup completed: ${BACKUP_DIR}/${SNAPSHOT_NAME}"
