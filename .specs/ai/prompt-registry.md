# AI Platform Specification: Prompt Registry & Management

## Overview
Prompts are versioned system configurations separate from application logic. This specification details dynamic templates loading and validations.

## Prompt Schema
Every prompt is defined as a YAML/JSON configuration file containing:
- `name`: String identifier.
- `version`: SemVer string (e.g. `1.0.0`).
- `description`: Summary of what the prompt accomplishes.
- `owner`: Team owning prompt.
- `system_template`: Mapped Jinja2 template string for system messages.
- `user_template`: Mapped Jinja2 template string for user messages.
- `variables`: List of required input variables names.
- `output_schema`: Optional validation schema structure.

## Versioning & Loading
- Dynamic registry matching name and version.
- Interpolates input variables using Jinja2 templates parsing.
- Asserts that all listed `variables` are provided at runtime, raising `PromptValidationError` on missing elements.
