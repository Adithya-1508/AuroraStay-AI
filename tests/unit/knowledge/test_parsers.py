from pathlib import Path

import pytest
from knowledge_platform.parsers import ParserFactory


@pytest.mark.asyncio
async def test_markdown_parser_async(tmp_path: Path) -> None:
    """Verifies that markdown parser extracts content and structure."""
    file_path = tmp_path / "test.md"
    file_path.write_text(
        "# Welcome\n\nThis is a test document v1.0.0.", encoding="utf-8"
    )

    factory = ParserFactory()
    parser = factory.get_parser(str(file_path))
    res = await parser.parse(str(file_path))

    assert "Welcome" in res["text"]
    assert res["metadata"]["type"] == "markdown"
    assert len(res["structure"]["headings"]) == 1
    assert res["structure"]["headings"][0] == "# Welcome"


@pytest.mark.asyncio
async def test_html_parser(tmp_path: Path) -> None:
    """Verifies that HTML parser strips tags."""
    file_path = tmp_path / "test.html"
    file_path.write_text("<html><body><h1>Hello</h1></body></html>", encoding="utf-8")

    factory = ParserFactory()
    parser = factory.get_parser(str(file_path))
    res = await parser.parse(str(file_path))

    assert res["text"] == "Hello"
    assert res["metadata"]["type"] == "html"


@pytest.mark.asyncio
async def test_csv_parser(tmp_path: Path) -> None:
    """Verifies that CSV parser extracts tabular rows."""
    file_path = tmp_path / "test.csv"
    file_path.write_text("name,role\nAlice,Manager\nBob,Staff", encoding="utf-8")

    factory = ParserFactory()
    parser = factory.get_parser(str(file_path))
    res = await parser.parse(str(file_path))

    assert "Alice, Manager" in res["text"]
    assert "Bob, Staff" in res["text"]
    assert res["metadata"]["type"] == "csv"
    assert res["structure"]["rows_count"] == 3


@pytest.mark.asyncio
async def test_json_parser(tmp_path: Path) -> None:
    """Verifies that JSON parser extracts key-values."""
    file_path = tmp_path / "test.json"
    file_path.write_text('{"hotel": "Grand", "rooms": 50}', encoding="utf-8")

    factory = ParserFactory()
    parser = factory.get_parser(str(file_path))
    res = await parser.parse(str(file_path))

    assert "Grand" in res["text"]
    assert "hotel" in res["structure"]["keys"]
    assert res["metadata"]["type"] == "json"
