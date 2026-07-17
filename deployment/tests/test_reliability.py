from unittest.mock import MagicMock

import pytest

from deployment.reliability.shutdown_handler import (
    GracefulShutdownHandler,
    dummy_cleanup,
)


def test_graceful_shutdown_handler() -> None:
    cleanup_mock = MagicMock()
    handler = GracefulShutdownHandler(cleanup_mock)

    # Trigger signal callback directly
    with pytest.raises(SystemExit) as e:
        handler._handle_sigterm(15, None)

    assert e.value.code == 0
    cleanup_mock.assert_called_once()
    assert handler.received_term is True


def test_dummy_cleanup_execution() -> None:
    # Verify execution of dummy cleanup does not raise exception
    dummy_cleanup()


def test_graceful_shutdown_handler_exception() -> None:
    def bad_cleanup() -> None:
        raise ValueError("cleanup error")

    handler = GracefulShutdownHandler(bad_cleanup)
    with pytest.raises(SystemExit) as e:
        handler._handle_sigterm(15, None)

    assert e.value.code == 0
    assert handler.received_term is True
