# Domain Value Objects

Value Objects are defined by their attributes and are fully immutable. This document specifies validation, equality, and structures for HospitalityAI's value objects.

---

## 1. Money
- **Attributes**: `amount` (Decimal), `currency` (String, e.g. "USD").
- **Validation**:
  - `amount` must be $\ge 0.00$.
  - `currency` must conform to ISO 4217 standard (three capital letters).
- **Equality Rules**: Equal if both `amount` and `currency` are identical.
- **Immutability**: Read-only properties. Operations (e.g. `add`, `multiply`) return a *new* instance of `Money`.

---

## 2. DateRange
- **Attributes**: `start_date` (Date), `end_date` (Date).
- **Validation**:
  - `end_date` must be at least 1 day after `start_date`.
- **Equality Rules**: Equal if both `start_date` and `end_date` are identical.
- **Helper Methods**:
  - `overlaps(other: DateRange) -> bool`: Checks date conflicts.
  - `duration_nights() -> int`: Returns difference in days.

---

## 3. RoomNumber
- **Attributes**: `value` (String, e.g. "302").
- **Validation**:
  - Must consist of 3-4 alphanumeric digits, where the first digits correspond to floor levels (e.g. "302" = floor 3).
- **Equality Rules**: Case-insensitive string match.

---

## 4. LoyaltyTier
- **Attributes**: `value` (String enum: Bronze, Silver, Gold, VIP).
- **Validation**:
  - Value must match one of the predefined levels.
- **Equality Rules**: Exact string comparison.

---

## 5. ConfidenceScore
- **Attributes**: `value` (Float).
- **Validation**:
  - Must satisfy $0.0 \le \text{value} \le 1.0$.
- **Equality Rules**: Floating-point comparison up to 4 decimal places.

---

## 6. LanguagePreference
- **Attributes**: `code` (String, e.g. "en", "es").
- **Validation**:
  - Must conform to ISO 639-1 two-character language codes.
- **Equality Rules**: Lowercase string comparison.
