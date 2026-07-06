# Personalized Recommendations Engine

The recommendation engine matches guest preferences, CRM loyalty levels, and active context to propose room upgrades, spa amenities, and dining opportunities.

## Recommendation Rules

| Offer Type | Rule Criteria | Example Output | Score |
| :--- | :--- | :--- | :--- |
| **Room Upgrade** | Loyalty Tier is `VIP` or `Platinum` | "Complimentary Suite Upgrade Offer" | `0.99` |
| **Vegetarian Dining** | Preferences contain `Vegetarian` or `Vegan` | "Vegetarian Dining at Aurora Bistro" | `0.95` |
| **Zen Spa Therapy** | Fallback standard for all guests | "Zen Premium Spa Therapy session" | `0.85` |

## Code Interface

```python
from business.guest.services.recommendations import RecommendationEngine

engine = RecommendationEngine(uow)

# Generate personalized recommendations
recs = await engine.generate_recommendations(guest_id)

# Fetch previously generated recommendations
previous_recs = await engine.get_guest_recommendations(guest_id)
```
