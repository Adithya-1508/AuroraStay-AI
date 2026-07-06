# Spec: Reservation Workflows and Tool Definitions

- **Status**: Draft
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-06

## 1. Purpose
Define the LangGraph workflow structures and tool input/output JSON schemas for executing reservation operations.

## 2. Responsibilities
- Orchestrate the multi-step workflows:
  - Create Reservation Workflow
  - Modify Reservation Workflow
  - Cancel Reservation Workflow
  - Upgrade Room Workflow
  - Check Availability Workflow
- Define input schemas and validation logic for tools.

## 3. Dependencies
- **LangGraph**: For step sequencing.
- **AI Core Tools**: Pydantic schemas for input validation.

## 4. Interfaces
### Tool Schemas
```python
# 1. SearchAvailabilityTool
class SearchAvailabilityInput(BaseModel):
    check_in_date: date
    check_out_date: date
    category_name: Optional[str] = None
    guests_count: int = 1

# 2. CalculatePriceTool
class CalculatePriceInput(BaseModel):
    category_name: str
    check_in_date: date
    check_out_date: date
    loyalty_tier: str = "Bronze"

# 3. ReserveRoomTool
class ReserveRoomInput(BaseModel):
    guest_id: UUID
    category_name: str
    check_in_date: date
    check_out_date: date
    special_requests: Optional[str] = None

# 4. ModifyReservationInput
class ModifyReservationInput(BaseModel):
    reservation_id: UUID
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    category_name: Optional[str] = None

# 5. CancelReservationInput
class CancelReservationInput(BaseModel):
    reservation_id: UUID
    reason: str

# 6. RecommendUpgradeInput
class RecommendUpgradeInput(BaseModel):
    reservation_id: UUID
```

### LangGraph Workflow Topology
Each workflow maps to a compiled LangGraph executing nodes sequentially:
- `planner_node`: Builds the step sequence.
- `executor_node`: Invokes target tools (requiring human confirmation on sensitive actions like cancellation/modification).
- `supervisor_node`: Validates output results and compliance checks.

## 5. Configuration
- `AUTO_APPROVE_SAFE_ACTIONS`: True (automatically runs search/pricing tools without prompting).
- `CONFIRM_SENSITIVE_ACTIONS`: True (halts execution before running write/delete tools).

## 6. Error Handling
- Invalid arguments trigger a Pydantic validation error returned directly to the agent planner.
- If a tool fails (e.g. database error), executor retries (up to 2 times) before marking step status as `FAILED`.

## 7. Security
- Tools enforce permissions checks:
  - `CancelReservationTool` requires `perm:cancel_reservation` or JWT owner matching.
  - `RecommendUpgradeTool` requires `perm:allocate_upgrades` or `Manager` context.

## 8. Testing
- **Workflow Simulation**:
  - Verify that the workflow halts on human-approval nodes when executing sensitive tools.
  - Assert that tool execution fails gracefully if inputs fail Pydantic model validation.

## 9. Acceptance Criteria
- [ ] Each of the 6 tools registers successfully with the `ToolExecutor`.
- [ ] Workflows correctly route from start node to end node.
- [ ] All inputs and outputs conform to strict JSON schemas.
