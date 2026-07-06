# RAG Specification: Retrieval Evaluation

This document details RAG retrieval metrics.

## Metrics Formulas

- **Retrieval Precision**: Ratio of relevant retrieved chunks to total retrieved chunks.
- **Retrieval Recall**: Ratio of relevant retrieved chunks to total relevant chunks in the golden dataset.
- **Context Relevance**: LLM-evaluated score measuring relevance of chunks to query.
- **Citation Accuracy**: Validates that all citations link to actual documents in the corpus and exist in the retrieved context.
- **Latency**: End-to-end retrieval and reranking duration in seconds.
