import importlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from knowledge_platform.indexing import QdrantIndexer
from knowledge_platform.reranking import NvidiaReranker

from knowledge_platform import ParserFactory


@pytest.mark.asyncio
async def test_qdrant_indexer_real_client() -> None:
    """Verifies that the Qdrant real client path calls APIs correctly."""
    mock_client = MagicMock()
    with patch("qdrant_client.QdrantClient", return_value=mock_client):
        indexer = QdrantIndexer(use_mock=False)
        assert indexer.use_mock is False

        await indexer.create_collection("test-col")
        mock_client.create_collection.assert_called_once()

        class MockChunk:
            chunk_id = "chunk-1"
            content = "hello"
            metadata = {"source": "test.txt", "version": "1.0"}

        await indexer.upsert_chunks("test-col", [MockChunk()], [[0.1] * 1536])
        mock_client.upsert.assert_called_once()

        mock_client.search.return_value = []
        res = await indexer.search("test-col", [0.1] * 1536)
        assert len(res) == 0
        mock_client.search.assert_called_once()


@pytest.mark.asyncio
async def test_nvidia_reranker_real_api() -> None:
    """Verifies Nvidia Reranker API calling and error fallbacks."""
    reranker = NvidiaReranker(api_key="test-api-key")
    assert reranker.api_key == "test-api-key"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rankings": [{"index": 0, "logit": 1.0}]}

    # Mock post call
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        res = await reranker.rerank("query", [{"content": "hello", "score": 0.5}])
        assert len(res) == 1
        assert res[0]["score"] > 0.5

    # Test error fallback
    mock_response.status_code = 500
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        res = await reranker.rerank("query", [{"content": "hello", "score": 0.5}])
        assert len(res) == 1


@pytest.mark.asyncio
async def test_pdf_docx_parsers(tmp_path: Path) -> None:
    """Verifies PDF and DOCX fallback parsers."""
    factory = ParserFactory()

    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_text("pdf content", encoding="utf-8")

    pdf_parser = factory.get_parser(str(pdf_path))
    pdf_res = await pdf_parser.parse(str(pdf_path))
    assert pdf_res["metadata"]["type"] == "pdf"

    docx_path = tmp_path / "test.docx"
    docx_path.write_text("docx content", encoding="utf-8")

    docx_parser = factory.get_parser(str(docx_path))
    docx_res = await docx_parser.parse(str(docx_path))
    assert docx_res["metadata"]["type"] == "docx"


def test_root_init() -> None:
    """Verifies that the hyphenated knowledge-platform __init__.py executes."""
    init_mod = importlib.import_module("knowledge-platform")
    assert init_mod.ParserFactory is not None
