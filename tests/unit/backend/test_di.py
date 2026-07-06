from backend.api.v1.dependencies import get_guest_repository, get_reservation_repository
from backend.repositories.guest import AbstractGuestRepository
from backend.repositories.reservation import AbstractReservationRepository


def test_dependency_injection_mappings() -> None:
    guest_repo = get_guest_repository()
    assert isinstance(guest_repo, AbstractGuestRepository)

    res_repo = get_reservation_repository()
    assert isinstance(res_repo, AbstractReservationRepository)
