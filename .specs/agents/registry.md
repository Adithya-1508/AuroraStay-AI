# Agent Specification: Agent Registry

This document details the registry system metadata standards.

## Registry Metadata Schema

Every registered agent publishes:
- `name`: Unique key identifier.
- `version`: SemVer-compliant version string.
- `description`: Purpose of the agent.
- `owner`: Responsible developer team tag.
- `capabilities`: Specific task capabilities list.
- `required_tools`: List of registered BaseTools required.
- `supported_workflows`: Workflows (e.g. `check_in`, `check_out`).
- `status`: Active, Deprecated, Testing.
