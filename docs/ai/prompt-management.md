# AI Platform: Prompt Management

This document details the configuration-driven versioning and compilation of prompt templates.

## Principles

- **Externalization**: Prompts are config assets stored in filesystem YAML files separate from Python code.
- **Jinja2 Rendering**: System and user templates support dynamic variables binding.
- **Strict Validations**: Registry checks that all variables declared in a prompt are passed at compile time, raising `ValueError` on omission.

## Prompt Yaml Example

```yaml
name: summarize
version: 1.0.0
description: Summarizes guest stay reviews.
system_template: "Summarize the review."
user_template: "Review: {{ review_text }}"
variables:
  - review_text
```
