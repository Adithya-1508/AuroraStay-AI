from typing import Any

import structlog

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.ops.services.operations import OperationsService
from business.reservation.events.publisher import (
    domain_event_publisher as res_publisher,
)
from business.reservation.events.schemas import ReservationCheckedOut

logger = structlog.get_logger()
ops_service = OperationsService()


async def handle_checkout_event(event: Any) -> None:
    """Listens to ReservationCheckedOut events and creates a housekeeping task."""
    if isinstance(event, ReservationCheckedOut):
        logger.info(
            "Handling ReservationCheckedOut event in Ops Context",
            reservation_id=str(event.reservation_id),
            room_id=str(event.room_id),
        )
        uow = PostgresUnitOfWork()
        try:
            async with uow:
                await ops_service.create_housekeeping_task(uow, event.room_id)
        except Exception as e:
            logger.error(
                "Failed to auto-create housekeeping task on checkout",
                error=str(e),
                room_id=str(event.room_id),
            )


# Subscribe the handler to the reservation event publisher
res_publisher.subscribe(handle_checkout_event)

__all__ = ["handle_checkout_event"]
