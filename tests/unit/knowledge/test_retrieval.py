from pathlib import Path

import pytest

from knowledge_platform import (
    EmbeddingPipeline,
    KnowledgeIngestionService,
    KnowledgeVersioningManager,
    NvidiaReranker,
    QdrantIndexer,
    RetrievalEvaluator,
    Retriever,
)


@pytest.mark.asyncio
async def test_end_to_end_rag_ingestion_and_retrieval(tmp_path: Path) -> None:
    """Verifies end-to-end ingestion, retrieval, reranking, and evaluation."""
    # 1. Initialize components
    indexer = QdrantIndexer(use_mock=True)
    embeddings = EmbeddingPipeline()
    versions = KnowledgeVersioningManager()

    ingest_service = KnowledgeIngestionService(indexer, embeddings, versions)
    retriever = Retriever(indexer, embeddings)
    reranker = NvidiaReranker(api_key=None)  # Uses fallback scorer
    evaluator = RetrievalEvaluator()

    # 2. Write temp document
    doc_path = tmp_path / "policies.md"
    doc_path.write_text(
        "# Guest Policies\n"
        "Check-in time is 3 PM.\n"
        "Checkout time is 11 AM.\n"
        "All rooms are non-smoking.",
        encoding="utf-8",
    )

    # 3. Ingest document
    doc_id = await ingest_service.ingest(
        file_path=str(doc_path), collection_name="test-policies", strategy="section"
    )
    assert doc_id is not None

    # 4. Verify version registered
    ver_record = versions.get_document_version(doc_id)
    assert ver_record is not None
    assert ver_record["document_version"] == "1.0.0"

    # 5. Retrieve chunks
    raw_results = await retriever.retrieve(
        query="What is the check-in time?", collection_name="test-policies", top_k=2
    )
    assert len(raw_results) > 0
    assert "Check-in" in raw_results[0]["content"]

    # 6. Rerank results
    reranked = await reranker.rerank(query="check-in time", chunks=raw_results)
    assert len(reranked) == len(raw_results)
    assert reranked[0]["score"] >= raw_results[0]["score"]

    # 7. Evaluate retrieval quality
    metrics = evaluator.evaluate_retrieval(
        retrieved_chunks=reranked,
        golden_chunk_ids=[reranked[0]["chunk_id"]],
        latency=0.045,
    )

    assert metrics["precision"] == 1.0 / len(reranked)
    assert metrics["recall"] == 1.0
    assert metrics["citation_accuracy"] == 1.0
    assert metrics["latency"] == 0.045

    # 8. Test evaluator with empty list
    empty_metrics = evaluator.evaluate_retrieval(
        retrieved_chunks=[], golden_chunk_ids=["chunk-1"], latency=0.01
    )
    assert empty_metrics["precision"] == 0.0
    assert empty_metrics["recall"] == 0.0
    assert empty_metrics["citation_accuracy"] == 1.0

    # 9. Test retriever query expansion hook
    async def dummy_expansion(q: str) -> str:
        return q + " check-in"

    retriever.register_query_expansion_hook(dummy_expansion)

    expanded_results = await retriever.retrieve(
        query="What is the time?", collection_name="test-policies", top_k=1
    )
    assert len(expanded_results) > 0

    # 10. Ingest file without version info
    no_ver_path = tmp_path / "nover.txt"
    no_ver_path.write_text("No versions here.", encoding="utf-8")
    no_ver_id = await ingest_service.ingest(
        file_path=str(no_ver_path), collection_name="test-policies"
    )
    assert no_ver_id is not None
    assert versions.get_document_version(no_ver_id)["document_version"] == "1.0.0"
