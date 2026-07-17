# Runbook: Knowledge Index Rebuilding

This runbook guides administrators through re-indexing raw document libraries into the Qdrant vector database.

## 1. Prerequisites

- Access to the OCI Object Storage bucket.
- Admin credentials for Qdrant API.

## 2. Re-indexing Steps

1. **Flush Corrupted Indexes**:
   Delete the corrupted Qdrant collection:
   ```bash
   curl -X DELETE http://localhost:6333/collections/hospitality_knowledge
   ```
2. **Re-create Collection**:
   Define vectors configuration (dimension 1536, cosine distance):
   ```bash
   # Create Qdrant collection API call
   ```
3. **Execute ETL Ingestion Job**:
   Trigger the document ingestion pipeline to re-download files from OCI Object Storage bucket and insert embeddings:
   ```bash
   python -m etl.ingest_docs --rebuild
   ```
4. **Verify Index Status**:
   Confirm collection count matches original document numbers:
   ```bash
   curl -s http://localhost:6333/collections/hospitality_knowledge
   ```
