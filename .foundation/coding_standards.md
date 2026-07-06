# Coding Standards

All code written in the HospitalityAI project must strictly adhere to these standards.

## Language and Runtime
- **Python 3.12+**: Use modern Python syntax and features (e.g., advanced type hinting, pattern matching, new generics syntax).

## Core Libraries & Frameworks
- **Pydantic v2**: Use for input/output validation, settings management, and data parsing.
- **SQLAlchemy 2.x**: Use async-style ORM interfaces for database interactions. No legacy 1.x styles.
- **FastAPI**: Use for high-performance REST APIs.
- **LangGraph**: Use for agent workflows.

## Formatting & Static Analysis
- **Ruff**: Standard linter and formatter. Must run on every commit.
- **Black**: Standard code formatter.
- **mypy**: Strict type-checking must pass. All type hints must be fully resolved.
- **pytest**: Core testing framework for unit and integration testing.

## Rules of Clean Code
- **Type Hints Everywhere**: Every function parameter and return type must be annotated. Avoid `Any` where possible.
- **Async-First**: All IO-bound operations (database queries, network requests, LLM calls) must use Python's async/await model.
- **No Global Mutable State**: Store state in database, cache (Redis), or instance objects. Global constants are allowed.
- **Zero Circular Imports**: Keep module boundaries clean. Use absolute imports.
- **No Duplicated Logic**: Extract shared helper functions and base structures.
- **Zero Hardcoded Secrets**: Use environment variables or configuration files.
- **No Giant Functions/Classes**: Keep modules small and focused on one responsibility.
- **No Commented-out Code or Dead Code**: Clean up unused code and remove placeholder comments before staging changes.
- **No Magic Numbers**: Define names/constants for values.
