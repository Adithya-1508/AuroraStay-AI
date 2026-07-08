class RevenueDomainError(Exception):
    """Base class for all exceptions in the revenue module."""

    pass


class ModelNotFoundError(RevenueDomainError):
    """Raised when a requested machine learning model cannot be found in registry."""

    pass


class ForecastingError(RevenueDomainError):
    """Raised when forecast generation fails or bounds are invalid."""

    pass


class DecisionNotFoundError(RevenueDomainError):
    """Raised when a decision package with the given ID cannot be found."""

    pass
