from knowledge_platform.citations import CitationGenerator


def test_citation_tag_generation_with_page() -> None:
    """Verifies that tag formatting includes version and page number."""
    generator = CitationGenerator()
    metadata = {
        "source": "c:/docs/housekeeping manual.pdf",
        "version": "2.0.1",
        "page": 5,
        "section": "Cleaning Procedures",
    }

    tag = generator.generate_tag(metadata)
    assert tag == "[housekeeping_manual_2_0_1_p5]"


def test_citation_tag_generation_without_page() -> None:
    """Verifies that tag formatting falls back to section name when page is missing."""
    generator = CitationGenerator()
    metadata = {
        "source": "c:/docs/guidelines.md",
        "version": "1.0.0",
        "section": "Safety Rules",
    }

    tag = generator.generate_tag(metadata)
    assert tag == "[guidelines_1_0_0_Safety_Rules]"


def test_format_citation() -> None:
    """Verifies that format_citation populates the citation dictionary structure."""
    generator = CitationGenerator()
    chunk = {
        "chunk_id": "chunk-1",
        "content": "Clean the floor.",
        "score": 0.95,
        "metadata": {
            "source": "manual.docx",
            "version": "1.0",
            "section": "Lobby",
        },
    }

    res = generator.format_citation(chunk)
    assert "citation" in res
    assert res["citation"]["source_document"] == "manual.docx"
    assert res["citation"]["confidence_score"] == 0.95
    assert res["citation"]["citation_tag"] == "[manual_1_0_Lobby]"
