from backend.ai.context.manager import ConversationContext


def test_context_history_trimming() -> None:
    """Verifies that context trims old non-system messages."""
    # Max tokens = 15
    ctx = ConversationContext(system_prompt="System Prompt", max_tokens=15)
    assert len(ctx.messages) == 1

    # Add messages
    ctx.add_message("user", "Hello first message")
    ctx.add_message("assistant", "Response first message")
    assert len(ctx.messages) == 3

    # Add massive message that triggers trimming
    ctx.add_message(
        "user",
        "A very long message that is extremely long.",
    )

    # First user/assistant messages should be trimmed
    assert len(ctx.messages) == 2
    assert ctx.messages[0]["role"] == "system"
    assert "extremely long" in ctx.messages[1]["content"]
