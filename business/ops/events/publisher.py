import structlog

from business.ops.events.schemas import OpsBaseEvent

logger = structlog.get_logger()


class OpsEventPublisher:
    """Publishes operations domain events to logs/streams."""

    def __init__(self) -> None:
        self.published_events: list[OpsBaseEvent] = []

    async def publish(self, event: OpsBaseEvent) -> None:
        """Dispatches the event payload to log records and registers in list."""
        self.published_events.append(event)
        logger.info(
            "Operations domain event published",
            event_type=event.__class__.__name__,
            event_id=str(event.event_id),
            timestamp=event.timestamp.isoformat(),
            payload=event.model_dump(),
        )


domain_event_publisher = OpsEventPublisher()

__all__ = ["OpsEventPublisher", "domain_event_publisher"]
