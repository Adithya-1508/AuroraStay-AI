from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class IdentityType(StrEnum):
    USER = "USER"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    AI_AGENT = "AI_AGENT"


class IdentityStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class Identity(BaseModel):
    identity_id: str
    type: IdentityType
    name: str
    owner: str
    status: IdentityStatus = IdentityStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime | None = None
    assigned_roles: list[str] = Field(default_factory=list)
    department: str
