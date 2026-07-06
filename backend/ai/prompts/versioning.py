import re


def validate_semver(version: str) -> bool:
    """Validates if a version string matches standard SemVer formats."""
    pattern = (
        r"^\d+\.\d+\.\d+"
        r"(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?"
        r"(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"
    )
    return bool(re.match(pattern, version))


__all__ = ["validate_semver"]
