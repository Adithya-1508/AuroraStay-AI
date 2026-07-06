from typing import Any


class ConversationContext:
    """Manages history, budgeting tokens to fit provider windows."""

    def __init__(
        self, system_prompt: str | None = None, max_tokens: int = 4000
    ) -> None:
        self.max_tokens = max_tokens
        self.messages: list[dict[str, Any]] = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add_message(self, role: str, content: str, **kwargs: Any) -> None:
        """Adds a message to history and runs budget trim audits."""
        self.messages.append({"role": role, "content": content, **kwargs})
        self.trim()

    def estimate_tokens(self) -> int:
        """Lightweight estimator approximating 4 characters per token."""
        char_count = 0
        for msg in self.messages:
            char_count += len(msg.get("content") or "")
        return char_count // 4

    def trim(self) -> None:
        """Removes the oldest non-system messages to fit context limits."""
        while self.estimate_tokens() > self.max_tokens and len(self.messages) > 1:
            removed = False
            for idx, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    self.messages.pop(idx)
                    removed = True
                    break
            if not removed:
                break


__all__ = ["ConversationContext"]
