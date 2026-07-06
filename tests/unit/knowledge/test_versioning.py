from knowledge_platform.versioning import KnowledgeVersioningManager


def test_version_registration_and_verification() -> None:
    """Verifies that version manager indexes and validates signatures correctly."""
    manager = KnowledgeVersioningManager()

    manager.register_version(
        document_id="doc-1",
        doc_version="1.0.0",
        embedding_version="nomic-v1",
        chunk_version="recursive_500",
        index_version="col-1",
    )

    record = manager.get_document_version("doc-1")
    assert record is not None
    assert record["document_version"] == "1.0.0"
    assert record["index_version"] == "col-1"

    # Matching check
    assert (
        manager.verify_versions(
            document_id="doc-1",
            doc_version="1.0.0",
            embedding_version="nomic-v1",
            chunk_version="recursive_500",
        )
        is True
    )

    # Mismatch check
    assert (
        manager.verify_versions(
            document_id="doc-1",
            doc_version="2.0.0",
            embedding_version="nomic-v1",
            chunk_version="recursive_500",
        )
        is False
    )
