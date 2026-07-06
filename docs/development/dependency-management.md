# Dependency Management with uv

HospitalityAI uses the modern `uv` package manager. Do not run standard pip commands unless inside a virtualenv.

## 1. Adding Dependencies
Add packages to the core `project.dependencies` list in [pyproject.toml](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/pyproject.toml) and sync your environment:
```bash
uv pip install <package_name>
```

## 2. Dev & Test Groups
Developer tools are separated into optional groups in `pyproject.toml`. To install them:
```bash
uv pip install -e .[dev,test]
```

## 3. Strict Rules
- Do not install unverified packages.
- Always run `mypy` after adding dependencies to check stub configurations.
