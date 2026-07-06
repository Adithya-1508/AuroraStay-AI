# Data Architecture

This document defines the storage layers of HospitalityAI, specifying relational database layouts, vector search collections, object storage buckets, and RAG/ETL pipelines.

## 1. Storage Technologies Layout

```
                        ┌───────────────────┐
                        │    Data Ingest    │ (CSV seeds, PDFs)
                        └─────────┬─────────┘
                                  │ ETL Pipelines
           ┌──────────────────────┼──────────────────────┐
           ▼                      ▼                      ▼
    ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
    │  PostgreSQL  │       │    Qdrant    │       │    MinIO     │
    │ (Relational) │       │   (Vector)   │       │   (Object)   │
    │  Guests,     │       │  FAQ Embed-  │       │  ML Models,  │
    │  Bookings,   │       │  dings       │       │  Ingested    │
    │  Tasks       │       │  Collection  │       │  PDFs        │
    └──────────────┘       └──────────────┘       └──────────────┘
```

---

## 2. Database Schema and Structures

### A. Relational Schema (PostgreSQL)
- **`guests`**: Unique guest identity, name, phone, loyalty metrics.
- **`room_types`**: Classification definitions (Single, Double, Deluxe, Suite), capacity boundaries, and baseline rates.
- **`rooms`**: Specific rooms mapping room numbers and cleaning/occupancy states.
- **`reservations`**: Calendar booking rows linking guests, rooms, nightly pricing rates, stay durations, and cancellation statuses.
- **`housekeeping_tasks`**: Tasks backlog monitoring clean/dirty rooms status, assignees, and completion speeds.
- **`review_sentiments`**: Records storing review texts, sentiment categories, and polarity values.

### B. Vector Schema (Qdrant)
- **Collection Name**: `hotel_faqs`
- **Vector Space**: Cosine similarity space (e.g. 1536 dimensions for standard text models).
- **Point Payload Schema**:
```json
{
  "chunk_id": "chk_302",
  "text": "The rooftop pool is open from 6:00 AM to 9:00 PM daily.",
  "metadata": {
    "source_file": "hotel_amenities_guide.pdf",
    "category": "pool_rules",
    "last_updated": "2026-07-04"
  }
}
```

### C. Object Storage Buckets (MinIO)
- **`ml-models`**: Holds binary weights and training parameter pickles for occupancy forecasts and cancellation classifiers.
- **`guest-documents`**: PDF files, menu images, and terms docs ingested into the RAG vectorizer.

---

## 3. RAG Indexing and Query Pipelines

```
  PDF Document ──> Parser ──> Semantic Chunker ──> Embedding Generator ──> Qdrant Index
```

1. **Parser**: Reads PDFs/text documents from MinIO.
2. **Chunker**: Splits texts into sentences, enforcing a overlap margin (e.g. 256 tokens chunk size, 32 tokens overlap).
3. **Embedding Generator**: Converts text chunks into high-dimensional vectors.
4. **Qdrant Index**: Loads points into the database, utilizing payload indexes for fast classification.
