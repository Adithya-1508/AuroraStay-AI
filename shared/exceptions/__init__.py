class HospitalityError(Exception):
    """Base exception class for all HospitalityAI errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BusinessRuleError(HospitalityError):
    """Raised when a business rule or aggregate invariant is violated."""

    pass


class EntityNotFoundError(HospitalityError):
    """Raised when a requested domain entity cannot be found."""

    pass


class AuthenticationError(HospitalityError):
    """Raised when security validation or access check fails."""

    pass
