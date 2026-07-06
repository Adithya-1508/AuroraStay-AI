class FeatureDefinition:
    """Metadata tracking features details inside the registry."""

    def __init__(
        self,
        name: str,
        owner: str,
        version: str,
        description: str,
        dependencies: list[str],
        source_dataset: str,
        refresh_frequency: str,
    ) -> None:
        self.name = name
        self.owner = owner
        self.version = version
        self.description = description
        self.dependencies = dependencies
        self.source_dataset = source_dataset
        self.refresh_frequency = refresh_frequency


class FeatureRegistry:
    """Registry keeping index collections of defined features."""

    def __init__(self) -> None:
        self.features: dict[str, FeatureDefinition] = {}

    def register_feature(self, feature: FeatureDefinition) -> None:
        """Adds a feature definition to the tracking catalog."""
        self.features[feature.name] = feature

    def get_feature(self, name: str) -> FeatureDefinition | None:
        """Retrieves a feature definition by its string identifier."""
        return self.features.get(name)

    def list_features(self) -> list[FeatureDefinition]:
        """Lists all registered features."""
        return list(self.features.values())


__all__ = ["FeatureDefinition", "FeatureRegistry"]
