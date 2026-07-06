import structlog

from business.guest.events.schemas import GuestBaseEvent

logger = structlog.get_logger()


class GuestEventPublisher:
    """Publishes guest domain events to logs/streams."""

    def __init__(self) -> None:
        self.published_events: list[GuestBaseEvent] = []

    async def publish(self, event: GuestBaseEvent) -> None:
        """Dispatches the event payload to log records and registers in list."""
        self.published_events.append(event)
        logger.info(
            "Guest domain event published",
            event_type=event.__class__.__name__,
            event_id=str(event.event_id),
            timestamp=event.timestamp.isoformat(),
            payload=event.model_dump(),
        )


domain_event_publisher = GuestEventPublisher()

__all__ = ["GuestEventPublisher", "domain_event_publisher"]
