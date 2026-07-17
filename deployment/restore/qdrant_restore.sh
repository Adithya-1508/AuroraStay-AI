#!/bin/bash
set -e

QDRANT_URL=${QDRANT_URL:-"http://localhost:6333"}
COLLECTION_NAME=${COLLECTION_NAME:-"hospitality_knowledge"}
SNAPSHOT_FILE=$1

if [ -z "${SNAPSHOT_FILE}" ]; then
  echo "Usage: $0 [path_to_snapshot_file.snapshot]"
  exit 1
fi

echo "Uploading vector collection snapshot to Qdrant server..."
curl -s -X POST -H "Content-Type: multipart/form-data" \
  -F "snapshot=@${SNAPSHOT_FILE}" \
  "${QDRANT_URL}/collections/${COLLECTION_NAME}/snapshots/upload"

echo "Restoring collection state from uploaded snapshot..."
SNAPSHOT_NAME=$(basename "${SNAPSHOT_FILE}")
curl -s -X POST "${QDRANT_URL}/collections/${COLLECTION_NAME}/snapshots/${SNAPSHOT_NAME}/recover"

echo "Qdrant collection state successfully restored."
