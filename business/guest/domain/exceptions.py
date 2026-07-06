class GuestDomainError(Exception):
    """Base exception for all guest domain errors."""

    pass


class GuestNotFoundError(GuestDomainError):
    """Raised when a guest cannot be found by ID or email."""

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Guest with identifier '{identifier}' was not found.")


class PreferenceUpdateError(GuestDomainError):
    """Raised when a preference update fails validation."""

    pass


class RecommendationError(GuestDomainError):
    """Raised when recommendation generation fails."""

    pass


class ConversationNotFoundError(GuestDomainError):
    """Raised when a conversation session is not found."""

    def __init__(self, session_id: str) -> None:
        super().__init__(f"Conversation session '{session_id}' was not found.")
