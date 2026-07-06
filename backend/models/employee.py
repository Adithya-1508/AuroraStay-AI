from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class Employee(Base, BaseEntity):
    """Employee table mapping database representation."""

    __tablename__ = "employees"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __mapper_args__ = {"version_id_col": version}


__all__ = ["Employee"]
