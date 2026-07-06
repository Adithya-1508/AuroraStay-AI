# Spec: Domain Value Objects

- **Status**: Ready
- **Owner**: Shared Domain Infrastructure (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines the base helper methods and validation criteria for value objects.

## 2. Responsibilities
- Ensure value object immutability.
- Map equality comparisons.

## 3. Public Interfaces
```python
class ValueObject(ABC):
    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return self.__dict__ == other.__dict__
```

## 4. Derived Specifications
Derived subclasses (e.g. `Money`, `DateRange`, `ConfidenceScore`) implement this interface, blocking mutations through setter locks.
