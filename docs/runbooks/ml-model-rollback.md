# Runbook: ML Model Version Rollback

This runbook guides administrators through rollback operations for active machine learning models.

## 1. Prerequisites

- Admin credentials to the MLflow Model Registry.
- Access to the target MLflow server console (Port 5000).

## 2. Revert Registered Model Version

1. **Query Model Registry**:
   Check currently active production version of the model:
   ```bash
   # Query MLflow registry for model tags
   ```
2. **Revert Active Tag**:
   Transition the compromised model version from `Production` to `Archived` stage.
3. **Promote Previous Version**:
   Transition the previous stable version (e.g. Version 2) from `Staging` to `Production` stage.
4. **Flush Cache**:
   Clear the local model cache inside backend pods to force reload of the new configuration.
