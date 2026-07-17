# Runbook: Agent Workflows Failures & Deadlocks

This runbook guides administrators through resolving LangGraph state graph deadlocks.

## 1. Diagnostics

- Check worker service logs for state errors:
  ```bash
  kubectl logs -l app=worker-agent -n hospitality
  ```
- Look for unhandled transitions or lock timeouts in state manager.

## 2. Re-triggering Workflows

1. **Clear Locked State**:
   If an agent thread is stuck in an infinite loop:
   - Identify the session thread ID from the logs.
   - Delete/reset the active state checkpoint inside the Redis/Postgres persistence store.
2. **Re-route Requests**:
   If the agent service fails completely:
   - Route incoming chat gateway calls to a fallback rule-based bot or alert human customer experience managers.
3. **Restart Worker Pods**:
   ```bash
   kubectl rollout restart deployment/worker-agent -n hospitality
   ```
