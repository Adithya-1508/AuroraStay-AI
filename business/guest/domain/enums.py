from enum import StrEnum


class LoyaltyTier(StrEnum):
    BRONZE = "Bronze"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    VIP = "VIP"


class SenderType(StrEnum):
    GUEST = "guest"
    ASSISTANT = "assistant"
    SYSTEM = "system"
