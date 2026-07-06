from knowledge_platform.chunking import ChunkingEngine


def test_fixed_size_split() -> None:
    """Verifies that fixed-size splitter segments text correctly."""
    engine = ChunkingEngine()
    text = "abcdefghij"
    # Chunk size 5, overlap 2
    # abcde, defgh, ghij
    res = engine.fixed_size_split(text, chunk_size=5, overlap=2)
    assert len(res) >= 2
    assert res[0] == "abcde"


def test_recursive_split() -> None:
    """Verifies that recursive character splitter preserves paragraphs and fits size."""
    engine = ChunkingEngine()
    text = "Hello world. This is paragraph one.\n\nParagraph two follows here."
    res = engine.recursive_split(text, chunk_size=40)
    assert len(res) == 2
    assert "one" in res[0]
    assert "two" in res[1]


def test_section_split() -> None:
    """Verifies that section splitter isolates headers and contents."""
    engine = ChunkingEngine()
    text = "# Header 1\nContent 1\n# Header 2\nContent 2"
    res = engine.section_split(text)
    assert len(res) == 2
    assert res[0]["header"] == "Header 1"
    assert res[0]["text"] == "Content 1"
    assert res[1]["header"] == "Header 2"
    assert res[1]["text"] == "Content 2"


def test_chunk_document() -> None:
    """Verifies that chunk_document attaches standard metadata properties."""
    engine = ChunkingEngine()
    text = "# Title\nWelcome here."

    chunks = engine.chunk_document(
        text=text,
        document_id="doc-123",
        source="doc.md",
        version="1.0.0",
        strategy="section",
    )

    assert len(chunks) == 1
    chunk = chunks[0]
    assert chunk.document_id == "doc-123"
    assert chunk.metadata["source"] == "doc.md"
    assert chunk.metadata["version"] == "1.0.0"
    assert chunk.metadata["heading"] == "Title"


def test_chunk_document_fixed_and_long_paragraph() -> None:
    """Verifies fixed-size chunking and long paragraph splits."""
    engine = ChunkingEngine()

    # 1. Test strategy="fixed"
    chunks_fixed = engine.chunk_document(
        text="abcdefghij",
        document_id="doc-fixed",
        source="doc.txt",
        version="1.0.0",
        strategy="fixed",
        chunk_size=5,
        overlap=2,
    )
    assert len(chunks_fixed) >= 2
    assert chunks_fixed[0].content == "abcde"

    # 2. Test recursive split with long paragraph triggering sentence-level split
    long_text = "This is sentence one. This is sentence two. This is sentence three."
    chunks_long = engine.chunk_document(
        text=long_text,
        document_id="doc-long",
        source="doc.txt",
        version="1.0.0",
        strategy="recursive",
        chunk_size=30,
        overlap=5,
    )
    assert len(chunks_long) > 1
