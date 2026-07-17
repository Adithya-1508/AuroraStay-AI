# Release Management & Rollback Procedures

This document covers release tags, upgrades strategies, and recovery rollback steps.

## 1. Rolling Deployments

We use standard rolling updates for zero-downtime releases:
- New pods are spun up in parallel with old pods.
- Load balancers route traffic to new pods only after they pass readiness checks.
- If a new pod crashes, the upgrade pauses, keeping old pods running.

## 2. Rollback Triggers

Rollbacks are triggered in two ways:
1. **Automated Rollback**: If liveness probes fail, the CI/CD pipeline executes:
   ```bash
   helm rollback hospitality-ai [PREVIOUS_REVISION]
   ```
2. **Manual Admin Rollback**: If production alerts highlight functional bugs post-release, administrators trigger a rollback via:
   ```bash
   curl -X POST http://hospitalityai.local/api/v1/deployment/rollback
   ```
   This invokes the deployment API router to revert the Helm chart release revision.
