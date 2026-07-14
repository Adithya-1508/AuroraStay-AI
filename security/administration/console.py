class AdminConsole:
    """Provides system controls, maintenance toggles, and AI asset approval gates."""

    def __init__(self) -> None:
        self.maintenance_mode = False
        # Approved registries
        self._approved_prompts: dict[str, str] = {}  # prompt_name -> status
        self._approved_models: dict[str, str] = {}  # model_name -> status

    def set_maintenance_mode(self, enabled: bool) -> None:
        self.maintenance_mode = enabled

    def register_prompt_approval(self, prompt_name: str, status: str) -> None:
        self._approved_prompts[prompt_name] = status

    def register_model_approval(self, model_name: str, status: str) -> None:
        self._approved_models[model_name] = status

    def is_prompt_approved(self, prompt_name: str) -> bool:
        return self._approved_prompts.get(prompt_name) == "APPROVED"

    def is_model_approved(self, model_name: str) -> bool:
        return self._approved_models.get(model_name) == "APPROVED"
