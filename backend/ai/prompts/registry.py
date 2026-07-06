import os
from typing import Any

import yaml
from jinja2 import Template


class PromptTemplate:
    """Represents a single versioned prompt template."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data["name"]
        self.version = data["version"]
        self.description = data.get("description", "")
        self.owner = data.get("owner", "")
        self.system_template = data.get("system_template", "")
        self.user_template = data.get("user_template", "")
        self.variables = data.get("variables", [])

    def render(self, variables: dict[str, Any]) -> list[dict[str, str]]:
        """Renders templates with variables, returning messages list."""
        for var in self.variables:
            if var not in variables:
                raise ValueError(f"Missing required prompt variable: '{var}'")

        system_content = Template(self.system_template).render(**variables)
        user_content = Template(self.user_template).render(**variables)

        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]


class PromptRegistry:
    """Registry managing filesystem loading of prompt configurations."""

    def __init__(self, templates_dir: str | None = None) -> None:
        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.templates_dir = templates_dir
        self._cache: dict[str, PromptTemplate] = {}

    def get(self, name: str) -> PromptTemplate:
        """Retrieves and compiles a prompt template by file name."""
        if name in self._cache:
            return self._cache[name]

        path = os.path.join(self.templates_dir, f"{name}.yaml")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prompt template '{name}' not found at {path}")

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            template = PromptTemplate(data)
            self._cache[name] = template
            return template


__all__ = ["PromptTemplate", "PromptRegistry"]
