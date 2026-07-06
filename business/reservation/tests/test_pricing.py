from datetime import date
from decimal import Decimal

from business.reservation.pricing.engine import PricingEngine


def test_pricing_engine_standard_night() -> None:
    """Verifies off-season weekday base rate stays (1 night)."""
    engine = PricingEngine()
    # Wednesday -> Thursday (no weekend markup) in May (no seasonal markup)
    check_in = date(2026, 5, 6)
    check_out = date(2026, 5, 7)
    base_price = 100.00

    cost = engine.calculate_price(
        base_nightly_price=base_price,
        check_in_date=check_in,
        check_out_date=check_out,
        loyalty_tier="Bronze",
    )

    assert cost.base_subtotal == Decimal("100.00")
    assert cost.seasonal_adjustments == Decimal("0.00")
    assert cost.weekend_adjustments == Decimal("0.00")
    assert cost.loyalty_discount == Decimal("0.00")
    assert cost.tax == Decimal("12.00")  # 12% of 100
    assert cost.total == Decimal("112.00")


def test_pricing_engine_weekend_night() -> None:
    """Verifies weekend nightly markups are applied (1.15 multiplier)."""
    engine = PricingEngine()
    # Friday -> Saturday night in May
    check_in = date(2026, 5, 8)
    check_out = date(2026, 5, 9)
    base_price = 100.00

    cost = engine.calculate_price(
        base_nightly_price=base_price,
        check_in_date=check_in,
        check_out_date=check_out,
        loyalty_tier="Bronze",
    )

    assert cost.base_subtotal == Decimal("100.00")
    # Weekend markup: +$15.00
    assert cost.weekend_adjustments == Decimal("15.00")
    assert cost.tax == Decimal("13.80")  # 12% of 115
    assert cost.total == Decimal("128.80")


def test_pricing_engine_summer_peak() -> None:
    """Verifies summer peak seasonal markup is applied (1.3 multiplier)."""
    engine = PricingEngine()
    # Wednesday -> Thursday night in July
    check_in = date(2026, 7, 8)
    check_out = date(2026, 7, 9)
    base_price = 100.00

    cost = engine.calculate_price(
        base_nightly_price=base_price,
        check_in_date=check_in,
        check_out_date=check_out,
        loyalty_tier="Bronze",
    )

    assert cost.base_subtotal == Decimal("100.00")
    # Summer seasonal markup: +$30.00
    assert cost.seasonal_adjustments == Decimal("30.00")
    assert cost.weekend_adjustments == Decimal("0.00")
    assert cost.total == Decimal("145.60")  # 130 * 1.12


def test_pricing_engine_loyalty_and_promo() -> None:
    """Verifies loyalty tier and promo discounts calculations."""
    engine = PricingEngine()
    # Wednesday -> Thursday night in May, Gold Tier (10%) + Promo WELCOME10 (10%)
    check_in = date(2026, 5, 6)
    check_out = date(2026, 5, 7)
    base_price = 200.00

    cost = engine.calculate_price(
        base_nightly_price=base_price,
        check_in_date=check_in,
        check_out_date=check_out,
        loyalty_tier="Gold",
        promo_code="WELCOME10",
    )

    assert cost.base_subtotal == Decimal("200.00")
    assert cost.loyalty_discount == Decimal("20.00")  # 10% of 200
    assert cost.promo_discount == Decimal("20.00")  # 10% of 200
    # Net: 200 - 20 - 20 = 160. Tax: 160 * 12% = 19.20. Total: 179.20.
    assert cost.tax == Decimal("19.20")
    assert cost.total == Decimal("179.20")
