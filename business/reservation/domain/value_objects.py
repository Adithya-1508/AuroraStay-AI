from datetime import date
from typing import Any

from pydantic import BaseModel, model_validator

from business.reservation.domain.exceptions import InvalidDateError


class BookingWindow(BaseModel):
    check_in_date: date
    check_out_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingWindow":
        if self.check_out_date <= self.check_in_date:
            raise InvalidDateError("Check-out date must be after check-in date.")
        return self

    @property
    def duration_nights(self) -> int:
        return (self.check_out_date - self.check_in_date).days


class GuestPreferences(BaseModel):
    pillow_type: str | None = None
    room_temperature: str | None = None
    special_requests: str | None = None
    extra_amenities: list[str] = []

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "GuestPreferences":
        if not data:
            return cls()
        return cls(
            pillow_type=data.get("pillow") or data.get("pillow_type"),
            room_temperature=data.get("temp") or data.get("room_temperature"),
            special_requests=data.get("special_requests"),
            extra_amenities=data.get("extra_amenities") or [],
        )


__all__ = ["BookingWindow", "GuestPreferences"]
