# RAG Specification: Reranker

This document outlines the reranker stage mapping inputs.

## Reranking Pipeline

To improve precision, raw retrieval results undergo secondary scoring:
1. Takes the query string and top-k retrieved chunks.
2. Passes them to a cross-encoder model (or provider rerank API).
3. Re-scores similarity matching context relevance.
4. Orders chunks descending by new similarity scores and returns pruned top-p results.
