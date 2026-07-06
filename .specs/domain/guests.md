# Spec: Guests Domain Aggregate

- **Status**: Ready
- **Owner**: Guest Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines the business attributes, preferences, and loyalty transitions for the `Guest` aggregate root.

## 2. Responsibilities
- Manage guest contact metadata and profile fields.
- Track customer loyalty status and room night counters.
- House CRM preferences (e.g. pillow type, temperature).

## 3. Public Interfaces
```python
class Guest:
    def __init__(self, guest_id: str, first_name: str, last_name: str, email: str, phone: str):
        self.guest_id = guest_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.loyalty_tier = LoyaltyTier("Bronze")
        self.completed_nights = 0
        self.preferences = GuestPreference(pillow="Standard", temperature=21.0)

    def increment_nights(self, nights_count: int) -> None:
        self.completed_nights += nights_count
        self.recalculate_loyalty_tier()

    def recalculate_loyalty_tier(self) -> None:
        if self.completed_nights >= 20:
            self.loyalty_tier = LoyaltyTier("VIP")
        elif self.completed_nights >= 10:
            self.loyalty_tier = LoyaltyTier("Gold")
        elif self.completed_nights >= 5:
            self.loyalty_tier = LoyaltyTier("Silver")
```

## 4. Invariants
- Each guest profile must declare a unique identifier.
- Loyalty progress night counters must be non-negative values.

## 5. Security & Validation
- Standard validation filters verifying that email address structures are correct.
