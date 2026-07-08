import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ModelRegistration(BaseModel):
    model_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    model_name: str
    version: str
    training_dataset: str
    metrics: dict[str, float] = Field(default_factory=dict)
    feature_set: list[str] = Field(default_factory=list)
    training_date: datetime = Field(default_factory=datetime.utcnow)
    owner: str
    deployment_status: str = "Candidate"  # Candidate, Production, Deprecated
    file_path: str | None = None


class ModelRegistry:
    """Registry tracking deployed and candidate ML model artifacts metadata."""

    def __init__(self) -> None:
        self._models: dict[uuid.UUID, ModelRegistration] = {}

    def register_model(self, registration: ModelRegistration) -> ModelRegistration:
        """Adds model metadata registration record."""
        self._models[registration.model_id] = registration
        return registration

    def get_model(self, model_id: uuid.UUID) -> ModelRegistration | None:
        """Retrieves a model registration by ID."""
        return self._models.get(model_id)

    def list_models(self) -> list[ModelRegistration]:
        """Returns all registered models."""
        return list(self._models.values())

    def get_latest_production(self, model_name: str) -> ModelRegistration | None:
        """Retrieves latest model marked as Production."""
        matches = [
            m
            for m in self._models.values()
            if m.model_name == model_name and m.deployment_status == "Production"
        ]
        if not matches:
            # Fallback to latest registered if no production
            matches = [m for m in self._models.values() if m.model_name == model_name]
        if not matches:
            return None
        # Return sorted by training date descending
        return sorted(matches, key=lambda x: x.training_date, reverse=True)[0]

    def promote_to_production(self, model_id: uuid.UUID) -> None:
        """Promotes model to Production and demotes old ones."""
        target = self.get_model(model_id)
        if not target:
            return

        # Demote existing production models under the same name
        for m in self._models.values():
            if (
                m.model_name == target.model_name
                and m.deployment_status == "Production"
            ):
                m.deployment_status = "Candidate"

        target.deployment_status = "Production"

    def rollback(self, model_name: str) -> ModelRegistration | None:
        """Rollbacks production status to the previous version."""
        candidates = sorted(
            [m for m in self._models.values() if m.model_name == model_name],
            key=lambda x: x.training_date,
            reverse=True,
        )
        if len(candidates) < 2:
            return None

        # Current active production
        current_prod = next(
            (m for m in candidates if m.deployment_status == "Production"), None
        )
        if current_prod:
            current_prod.deployment_status = "Candidate"

        # Promote previous one
        prev_model = candidates[1] if current_prod == candidates[0] else candidates[0]
        prev_model.deployment_status = "Production"
        return prev_model
