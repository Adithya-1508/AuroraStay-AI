# Personalized Upsell & Cross-sell

The `RecommendationService` calculates personalized suggestions for incoming and existing guests.

## Room Upsells
- **Algorithm**: Inspects the guest's booked category and checks the available list of categories. If a higher-tier room category (with a higher base price) exists, it recommends the next-cheapest room upgrade.
- **Price Delta**: Calculates the incremental cost required to upgrade, facilitating easy decision-making for the guest.
- **Persistence**: Upsell recommendations are saved in the `recommendations` table for downstream conversions tracking.

## Ancillary Cross-sells
- **Swedish Massage Discount (Spa Offer)**: Triggered dynamically if spa facilities are configured.
- **Fine Dining Wine Pairing (Restaurant Offer)**: Promotes food and beverage conversions.
