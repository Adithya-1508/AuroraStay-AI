from enum import StrEnum


class UserRole(StrEnum):
    GUEST = "Guest"
    STAFF = "Staff"
    MANAGER = "Manager"
    ADMINISTRATOR = "Administrator"
    AI_SERVICE = "AIService"
    WORKER = "Worker"
