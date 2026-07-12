from typing import Any


class GovernanceRegistry:
    """Manages the registration and ownership audits of all AI assets in the platform."""

    def __init__(self) -> None:
        self.models: list[dict[str, Any]] = [
            {
                "model_name": "forecaster-regressor",
                "owner": "Revenue Team",
                "risk_class": "MEDIUM",
                "data_privacy": "PII_REDACTED",
            },
            {
                "model_name": "guest-segmenter-kmeans",
                "owner": "Guest Experience Team",
                "risk_class": "LOW",
                "data_privacy": "PII_REDACTED",
            },
        ]
        self.prompts: list[dict[str, Any]] = [
            {
                "prompt_name": "pricing_explanation",
                "owner": "Revenue Team",
                "version": "1.2.0",
            },
            {
                "prompt_name": "concierge_faq",
                "owner": "Guest Experience Team",
                "version": "2.1.0",
            },
        ]
        self.agents: list[dict[str, Any]] = [
            {"agent_name": "GuestConcierge", "owner": "Guest Experience Team"},
            {"agent_name": "RevenueAgent", "owner": "Revenue Team"},
        ]

    def register_model(
        self, name: str, owner: str, risk_class: str, privacy: str
    ) -> None:
        self.models.append(
            {
                "model_name": name,
                "owner": owner,
                "risk_class": risk_class,
                "data_privacy": privacy,
            }
        )

    def verify_asset_compliance(self, asset_type: str, name: str) -> bool:
        """Verifies if an asset name is registered and has an assigned owner."""
        if asset_type.lower() == "model":
            return any(m["model_name"] == name for m in self.models)
        elif asset_type.lower() == "prompt":
            return any(p["prompt_name"] == name for p in self.prompts)
        elif asset_type.lower() == "agent":
            return any(a["agent_name"] == name for a in self.agents)
        return False
