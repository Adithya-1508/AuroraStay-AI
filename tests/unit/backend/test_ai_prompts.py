import pytest

from backend.ai.prompts.registry import PromptRegistry
from backend.ai.prompts.versioning import validate_semver


def test_prompt_template_rendering() -> None:
    """Verifies that templates render variables and check for missing ones."""
    registry = PromptRegistry()
    template = registry.get("summarize")

    # Correct render
    messages = template.render({"review_text": "Clean rooms."})
    assert len(messages) == 2
    assert "Clean rooms." in messages[1]["content"]

    # Missing variables error
    with pytest.raises(ValueError, match="Missing required prompt variable"):
        template.render({})


def test_semver_validator() -> None:
    """Verifies that prompt version strings match SemVer specifications."""
    assert validate_semver("1.0.0") is True
    assert validate_semver("2.5.12-alpha.1") is True
    assert validate_semver("invalid-version") is False
