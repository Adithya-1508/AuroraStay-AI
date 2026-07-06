# Spec: Environment Configuration Management

- **Status**: Ready
- **Owner**: Infrastructure Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines environment settings loading, default parameters, and schemas.

## 2. Variables Configurations

| Key | Type | Default Value | Validation Limits |
| --- | --- | --- | --- |
| **DATABASE_URL** | String | `postgresql+asyncpg://.../hospitality` | Must use `postgresql+asyncpg` scheme. |
| **REDIS_URL** | String | `redis://localhost:6379/0` | Must use `redis` scheme. |
| **QDRANT_URL** | String | `http://localhost:6333` | Valid HTTP endpoint. |
| **JWT_SECRET** | String | `supersecretkeychangeinproduction` | Min length 32 characters in production. |
| **MODEL_PROVIDER** | String | `gemini` | Enum: `gemini`, `nvidia`, `ollama`. |
| **LOG_LEVEL** | String | `INFO` | Enum: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
