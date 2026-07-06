# Reranker Stage Manual

The `NvidiaReranker` implements the `nvidia/rerank-qa-mistral-4b` model to re-score retrieval results.

## Fallback Logic

If the `NVIDIA_API_KEY` is absent, the rerank stage falls back to a local term-overlap similarity scorer, preventing service interruptions.
