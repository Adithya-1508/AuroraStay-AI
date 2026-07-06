from abc import abstractmethod
from collections.abc import Sequence

from backend.models.room import Room, RoomCategory
from backend.repositories.base import AbstractRepository


class AbstractRoomCategoryRepository(AbstractRepository[RoomCategory]):
    """Abstract interface defining behaviors for RoomCategory persistence."""

    @abstractmethod
    async def get_by_name(self, name: str) -> RoomCategory | None:
        """Retrieves a room category by its name."""
        pass


class AbstractRoomRepository(AbstractRepository[Room]):
    """Abstract interface defining behaviors for Room persistence."""

    @abstractmethod
    async def get_by_room_number(self, room_number: str) -> Room | None:
        """Retrieves a room record by its physical room number."""
        pass

    @abstractmethod
    async def get_by_category(self, category_id: str) -> Sequence[Room]:
        """Retrieves all room records associated with a category."""
        pass


__all__ = ["AbstractRoomCategoryRepository", "AbstractRoomRepository"]
