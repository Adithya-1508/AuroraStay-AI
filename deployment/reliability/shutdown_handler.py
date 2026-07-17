import signal
import sys
import time
from collections.abc import Callable
from typing import Any


class GracefulShutdownHandler:
    """Listens for termination signals to drain connection pools and active requests."""

    def __init__(self, cleanup_callback: Callable[[], None]) -> None:
        self.cleanup_callback = cleanup_callback
        self.received_term = False
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)

    def _handle_sigterm(self, signum: int, frame: Any) -> None:
        """Triggers process cleanup and exits code cleanly."""
        print(f"Received signal {signum}. Commencing graceful shutdown...")
        self.received_term = True
        try:
            self.cleanup_callback()
        except Exception as e:
            print(f"Error during cleanup callback execution: {str(e)}")
        print("Shutdown process complete. Exiting.")
        sys.exit(0)


def dummy_cleanup() -> None:
    print("Draining active SQL connection pools...")
    time.sleep(0.5)
    print("Connection pools cleared.")
