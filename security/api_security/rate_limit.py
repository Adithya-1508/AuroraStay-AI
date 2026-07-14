import time


class SlidingWindowRateLimiter:
    """In-memory sliding window rate limiter for API endpoint security."""

    def __init__(self, window_seconds: int = 60, max_requests: int = 60) -> None:
        self.window_seconds = window_seconds
        self.max_requests = max_requests
        # Maps client identifier -> list of timestamps
        self.request_history: dict[str, list[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        """Determines if the request from the client falls within the allowed rate limits."""
        now = time.time()
        cutoff = now - self.window_seconds

        # Get or create sliding history
        history = self.request_history.get(client_id, [])

        # Filter out timestamps older than the window duration
        filtered_history = [t for t in history if t > cutoff]

        if len(filtered_history) >= self.max_requests:
            self.request_history[client_id] = filtered_history
            return False

        # Add current timestamp
        filtered_history.append(now)
        self.request_history[client_id] = filtered_history
        return True

    def reset_limits(self, client_id: str) -> None:
        """Clears client history records."""
        if client_id in self.request_history:
            del self.request_history[client_id]
