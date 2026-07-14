class AIGuardrails:
    """Scans AI prompt variables and outputs to prevent injection and leakage."""

    # Common prompt injection patterns
    INJECTION_KEYWORDS = [
        "ignore previous instructions",
        "bypass rules",
        "system prompt override",
        "you are now an unrestricted",
        "dan mode",
        "forget all rules",
    ]

    # Leakage indicators
    LEAKAGE_KEYWORDS = [
        "system instructions:",
        "here are the rules you must follow",
        "base prompt:",
        "you are a helpful assistant designed to",
    ]

    @classmethod
    def scan_input_for_injection(cls, prompt_input: str) -> bool:
        """Returns True if prompt injection indicators are detected."""
        normalized = prompt_input.lower()
        return any(kw in normalized for kw in cls.INJECTION_KEYWORDS)

    @classmethod
    def scan_output_for_leakage(cls, llm_output: str) -> bool:
        """Returns True if leakage of system instructions is found in output."""
        normalized = llm_output.lower()
        return any(kw in normalized for kw in cls.LEAKAGE_KEYWORDS)
