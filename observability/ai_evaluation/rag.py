import re


class RAGEvaluator:
    """Calculates retrieval, groundedness, and citation metrics for RAG pipelines."""

    @staticmethod
    def evaluate_groundedness(output_text: str, context_text: str) -> float:
        """Computes fraction of output words present in the source context text."""
        # Simple token overlap ratio ignoring punctuation and case
        out_words = re.findall(r"\w+", output_text.lower())
        ctx_words = set(re.findall(r"\w+", context_text.lower()))

        if not out_words:
            return 1.0

        matched = sum(1 for w in out_words if w in ctx_words)
        return float(matched / len(out_words))

    @staticmethod
    def evaluate_retrieval(
        retrieved_ids: list[str], ground_truth_ids: list[str]
    ) -> dict[str, float]:
        """Calculates precision and recall on chunk IDs."""
        if not retrieved_ids or not ground_truth_ids:
            return {"precision": 1.0, "recall": 1.0}

        ret_set = set(retrieved_ids)
        gt_set = set(ground_truth_ids)

        hits = len(ret_set.intersection(gt_set))
        return {
            "precision": float(hits / len(ret_set)),
            "recall": float(hits / len(gt_set)),
        }

    @staticmethod
    def evaluate_citations(output_text: str, source_urls: list[str]) -> float:
        """Verifies if the cited links exist in the source document list."""
        citations = re.findall(r"\[([^\]]+)\]\((file:///[^\)]+)\)", output_text)
        if not citations:
            return 1.0  # no citation is technically accurate if not needed

        valid = 0
        for _label, url in citations:
            if url in source_urls:
                valid += 1

        return float(valid / len(citations))
