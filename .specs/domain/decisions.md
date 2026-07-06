# Spec: Decisions Domain Aggregate

- **Status**: Ready
- **Owner**: Decision Intelligence Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define decision parameters linking to system recommendations, logging approval state changes.

## 2. Responsibilities
- Record decision resolutions (Approved/Rejected).
- Track decision creator identities (staff/admin) and reasoning.

## 3. Public Interfaces
```python
class Decision:
    def __init__(self, decision_id: str, recommendation_id: str, staff_id: str, resolution: str, notes: str):
        self.decision_id = decision_id
        self.recommendation_id = recommendation_id
        self.staff_id = staff_id
        self.resolution = resolution  # 'Approved' or 'Rejected'
        self.notes = notes
        self.executed_at = datetime.utcnow()
```

## 4. Invariants
- Decisions must reference a valid Recommendation ID.
