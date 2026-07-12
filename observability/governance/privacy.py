import re


class PIIRedactor:
    """Filters personal identifiable information from prompt variables to protect privacy."""

    # Simple email pattern
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    # Phone pattern: matches (123) 456-7890, 123-456-7890, +1 1234567890 etc.
    PHONE_REGEX = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

    @classmethod
    def redact_text(cls, text: str) -> str:
        """Redacts emails and phone numbers from raw strings."""
        redacted = cls.EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
        redacted = cls.PHONE_REGEX.sub("[REDACTED_PHONE]", redacted)
        return redacted
