# RAG Evaluation Manual

## Overview
Retrieval-Augmented Generation (RAG) is monitored continuously to verify that generated insights are truthful, factual, and strictly supported by source documents.

## Metrics
1. **Groundedness**: Overlap ratio of output words present in the retrieved context chunks.
2. **Retrieval Precision**: Ratio of relevant chunks retrieved to total fetched chunks.
3. **Retrieval Recall**: Ability to find all relevant guidelines for the query context.
4. **Citation Accuracy**: Verifies if the cited source link exists in the retrieved documents list.

## REST API
- **POST** `/api/v1/observability/evaluate`
  - Body: `{ "evaluation_type": "RAG", "predictions": ["output"], "actuals": ["context"] }`
  - Response: Evaluated groundedness metric.
