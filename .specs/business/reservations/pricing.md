# Spec: Pricing Engine

- **Status**: Draft
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-06

## 1. Purpose
Define the business rules and math for calculating nightly and total costs for reservations, including multipliers, discounts, and taxes.

## 2. Responsibilities
- Calculate base costs per night for a given room category.
- Apply seasonal multipliers (peak summer, winter holidays).
- Apply weekend markups.
- Calculate guest discounts based on loyalty tiers (Bronze, Silver, Gold, Platinum).
- Calculate final taxes.

## 3. Dependencies
- **Guest Profile**: Loyalty tier checks.
- **Config / Settings**: Active pricing rates and multipliers.

## 4. Interfaces
```python
class PricingEngine:
    def calculate_total_price(
        self,
        base_nightly_price: Decimal,
        window: BookingWindow,
        loyalty_tier: str,
        promo_code: Optional[str] = None
    ) -> ReservationCostBreakdown:
        """Computes step-by-step price breakdown of stay."""
        pass
```

### Pricing Formula
$$\text{Cost} = \sum_{d \in \text{days}} \left( \text{BasePrice} \times \text{SeasonalMultiplier}(d) \times \text{WeekendMultiplier}(d) \right)$$
$$\text{DiscountedCost} = \text{Cost} \times (1 - \text{LoyaltyDiscount} - \text{PromoDiscount})$$
$$\text{FinalPrice} = \text{DiscountedCost} \times (1 + \text{TaxRate})$$

## 5. Configuration
- `SEASONAL_MULTIPLIERS`:
  - Summer (Jun-Aug): 1.3
  - Holidays (Dec 15 - Jan 5): 1.5
  - Default: 1.0
- `WEEKEND_MULTIPLIER` (Fri/Sat nights): 1.15
- `LOYALTY_DISCOUNTS`:
  - Bronze: 0.0
  - Silver: 0.05
  - Gold: 0.10
  - Platinum: 0.15
- `TAX_RATE`: 0.12 (12%)

## 6. Error Handling
- `InvalidPromoCodeException`: Warning raised, fallback to standard calculations.

## 7. Security
- Pricing adjustments (custom discounts) require manager authentication.

## 8. Testing
- **Unit Tests**:
  - Assert pricing calculations match manual expectations for simple stays, weekend stays, holiday stays, and multi-tier loyalty discounts.

## 9. Acceptance Criteria
- [ ] Stays traversing a weekend apply weekend multipliers only to the weekend nights.
- [ ] Loyalty tier discounts are correctly applied to the pre-tax total.
- [ ] Full breakdown of prices is returned (base, adjustments, taxes, total).
