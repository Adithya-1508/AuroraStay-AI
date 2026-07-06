from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


@dataclass
class CostBreakdown:
    base_subtotal: Decimal
    seasonal_adjustments: Decimal
    weekend_adjustments: Decimal
    loyalty_discount: Decimal
    promo_discount: Decimal
    tax: Decimal
    total: Decimal


class PricingEngine:
    """Computes room reservation rates applying seasonality, weekends, loyalty, and taxes."""

    def __init__(
        self,
        summer_multiplier: float = 1.3,
        holiday_multiplier: float = 1.5,
        weekend_multiplier: float = 1.15,
        tax_rate: float = 0.12,
    ) -> None:
        self.summer_multiplier = Decimal(str(summer_multiplier))
        self.holiday_multiplier = Decimal(str(holiday_multiplier))
        self.weekend_multiplier = Decimal(str(weekend_multiplier))
        self.tax_rate = Decimal(str(tax_rate))

    def _get_date_multiplier(self, day: date) -> Decimal:
        """Determines seasonal multipliers based on specific calendar dates."""
        # Summer Season: June 1st - August 31st
        if 6 <= day.month <= 8:
            return self.summer_multiplier
        # Holiday Season: December 15th - January 5th
        if (day.month == 12 and day.day >= 15) or (day.month == 1 and day.day <= 5):
            return self.holiday_multiplier
        return Decimal("1.0")

    def _is_weekend(self, day: date) -> bool:
        """Friday and Saturday nights are considered weekend nights."""
        # Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6
        return day.weekday() in (4, 5)

    def calculate_price(
        self,
        base_nightly_price: float | Decimal,
        check_in_date: date,
        check_out_date: date,
        loyalty_tier: str = "Bronze",
        promo_code: str | None = None,
    ) -> CostBreakdown:
        """Calculates step-by-step cost breakdown for the given stay parameters."""
        base_price = Decimal(str(base_nightly_price))
        total_days = (check_out_date - check_in_date).days

        if total_days <= 0:
            return CostBreakdown(
                base_subtotal=Decimal("0.0"),
                seasonal_adjustments=Decimal("0.0"),
                weekend_adjustments=Decimal("0.0"),
                loyalty_discount=Decimal("0.0"),
                promo_discount=Decimal("0.0"),
                tax=Decimal("0.0"),
                total=Decimal("0.0"),
            )

        base_subtotal = Decimal("0.0")
        seasonal_adjustments = Decimal("0.0")
        weekend_adjustments = Decimal("0.0")

        current_date = check_in_date
        while current_date < check_out_date:
            daily_base = base_price
            base_subtotal += daily_base

            # 1. Seasonality
            multiplier = self._get_date_multiplier(current_date)
            daily_seasonal_diff = (daily_base * multiplier) - daily_base
            seasonal_adjustments += daily_seasonal_diff

            # 2. Weekend markups
            if self._is_weekend(current_date):
                daily_weekend_diff = (
                    daily_base * multiplier * self.weekend_multiplier
                ) - (daily_base * multiplier)
                weekend_adjustments += daily_weekend_diff

            current_date += timedelta(days=1)

        subtotal_pre_discount = (
            base_subtotal + seasonal_adjustments + weekend_adjustments
        )

        # 3. Loyalty Discount
        loyalty_rate = Decimal("0.0")
        tier = loyalty_tier.strip().capitalize()
        if tier == "Silver":
            loyalty_rate = Decimal("0.05")
        elif tier == "Gold":
            loyalty_rate = Decimal("0.10")
        elif tier == "Platinum":
            loyalty_rate = Decimal("0.15")

        loyalty_discount = subtotal_pre_discount * loyalty_rate

        # 4. Promo Discount
        promo_rate = Decimal("0.0")
        if promo_code and promo_code.strip().upper() == "WELCOME10":
            promo_rate = Decimal("0.10")

        promo_discount = subtotal_pre_discount * promo_rate

        net_pre_tax = subtotal_pre_discount - loyalty_discount - promo_discount
        if net_pre_tax < 0:
            net_pre_tax = Decimal("0.0")

        # 5. Taxes
        tax = net_pre_tax * self.tax_rate
        total = net_pre_tax + tax

        return CostBreakdown(
            base_subtotal=base_subtotal.quantize(Decimal("0.01")),
            seasonal_adjustments=seasonal_adjustments.quantize(Decimal("0.01")),
            weekend_adjustments=weekend_adjustments.quantize(Decimal("0.01")),
            loyalty_discount=loyalty_discount.quantize(Decimal("0.01")),
            promo_discount=promo_discount.quantize(Decimal("0.01")),
            tax=tax.quantize(Decimal("0.01")),
            total=total.quantize(Decimal("0.01")),
        )


__all__ = ["PricingEngine", "CostBreakdown"]
