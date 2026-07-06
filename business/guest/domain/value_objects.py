from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProfileDetails:
    first_name: str
    last_name: str
    email: str
    phone: str | None = None

    def __post_init__(self) -> None:
        if not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email address format")


@dataclass(frozen=True)
class PreferenceSet:
    room_preferences: dict[str, str] = field(default_factory=dict)
    pillow_preferences: str | None = None
    dietary_restrictions: list[str] = field(default_factory=list)
    accessibility_requirements: list[str] = field(default_factory=list)
    communication_preferences: dict[str, str] = field(default_factory=dict)
