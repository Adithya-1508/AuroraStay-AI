from typing import Any


class RetrievalEvaluator:
    """Evaluates retrieval precision, recall, and citation metrics."""

    def evaluate_retrieval(
        self,
        retrieved_chunks: list[dict[str, Any]],
        golden_chunk_ids: list[str],
        latency: float,
    ) -> dict[str, Any]:
        """Computes precision, recall, relevance, and citation alignment accuracy."""
        retrieved_ids = [c["chunk_id"] for c in retrieved_chunks]

        hits = [rid for rid in retrieved_ids if rid in golden_chunk_ids]
        precision = len(hits) / len(retrieved_ids) if retrieved_ids else 0.0
        recall = len(hits) / len(golden_chunk_ids) if golden_chunk_ids else 0.0

        avg_score = (
            sum(c.get("score", 0.0) for c in retrieved_chunks) / len(retrieved_chunks)
            if retrieved_chunks
            else 0.0
        )

        citation_errors = 0
        for c in retrieved_chunks:
            meta = c.get("metadata", {})
            if not meta.get("source") or not meta.get("version"):
                citation_errors += 1

        citation_accuracy = (
            1.0 - (citation_errors / len(retrieved_chunks)) if retrieved_chunks else 1.0
        )

        return {
            "precision": precision,
            "recall": recall,
            "context_relevance": avg_score,
            "citation_accuracy": citation_accuracy,
            "latency": latency,
        }


__all__ = ["RetrievalEvaluator"]
