from backend.feature_store.registry.registry import (
    FeatureDefinition,
    FeatureRegistry,
)


def setup_feature_registry() -> FeatureRegistry:
    """Pre-populates the registry with target metadata for planned ML features."""
    registry = FeatureRegistry()

    # 1. Register Guest Stay Frequency feature metadata
    registry.register_feature(
        FeatureDefinition(
            name="guest_stay_frequency",
            owner="Loyalty Engineering Team",
            version="1.0.0",
            description="Tracks historical reservation booking counts for guests.",
            dependencies=["reservations.id"],
            source_dataset="reservations",
            refresh_frequency="Daily",
        )
    )

    # 2. Register Guest Total Spend feature metadata
    registry.register_feature(
        FeatureDefinition(
            name="guest_total_spend",
            owner="Revenue Management Team",
            version="1.0.0",
            description="Calculates cumulative payment spend across all bookings.",
            dependencies=["reservations.total_cost"],
            source_dataset="reservations",
            refresh_frequency="Daily",
        )
    )

    return registry


__all__ = ["setup_feature_registry"]
