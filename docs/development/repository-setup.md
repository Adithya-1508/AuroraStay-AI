# Repository Setup Guide

Follow these steps to bootstrap your local environment for HospitalityAI:

## 1. Prerequisites
- **Python**: Installed version $\ge 3.12$.
- **uv**: Astral's package manager. Install it via:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Docker**: Docker Desktop (or engine) running.

## 2. Environment Verification
Run the bootstrap python script to verify directory structures and copy `.env.example` configurations to your local `.env`:
```bash
python scripts/bootstrap.py
```

## 3. Dependency Installation
Create your virtual environment and install dependency groups (dev, test, ml) using `uv`:
```bash
uv venv
uv pip install -e .[dev,test,ml]
```

## 4. Install Git Hooks
Configure pre-commit hooks to automate formatting and typing checks on commit:
```bash
pre-commit install
```
