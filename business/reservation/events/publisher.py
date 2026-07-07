import structlog

from business.reservation.events.schemas import ReservationBaseEvent

from collections.abc import Awaitable, Callable

logger = structlog.get_logger()


class EventPublisher:
    """Publishes domain events to logs/streams for future asynchronous consumer platforms."""

    def __init__(self) -> None:
        self.published_events: list[ReservationBaseEvent] = []
        self.subscribers: list[Callable[[ReservationBaseEvent], Awaitable[None]]] = []

    def subscribe(
        self, callback: Callable[[ReservationBaseEvent], Awaitable[None]]
    ) -> None:
        """Registers a callback handler for published events."""
        self.subscribers.append(callback)

    async def publish(self, event: ReservationBaseEvent) -> None:
        """Dispatches the event payload to log records and registers in list."""
        self.published_events.append(event)
        logger.info(
            "Reservation domain event published",
            event_type=event.__class__.__name__,
            event_id=str(event.event_id),
            timestamp=event.timestamp.isoformat(),
            payload=event.model_dump(),
        )
        for subscriber in self.subscribers:
            try:
                await subscriber(event)
            except Exception as e:
                logger.error(
                    "Error in reservation event subscriber",
                    error=str(e),
                    event_type=event.__class__.__name__,
                )


# Global publisher instance
domain_event_publisher = EventPublisher()

__all__ = ["EventPublisher", "domain_event_publisher"]
