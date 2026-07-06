from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from backend.ai.tools.executor import BaseTool, ToolExecutor


class DummyInput(BaseModel):
    value: int


class DummyTool(BaseTool):
    name = "dummy_tool"
    description = "A dummy test tool."
    args_schema = DummyInput
    permissions = ["admin_scope"]

    async def _run(self, **kwargs: Any) -> str:
        value = kwargs["value"]
        return f"Result: {value}"


@pytest.mark.asyncio
async def test_tool_arguments_validation() -> None:
    """Verifies that tool execute throws validation error on bad arguments type."""
    tool = DummyTool()

    # Good parameter
    res = await tool.execute(value=42)
    assert res == "Result: 42"

    # Bad parameter
    with pytest.raises(ValidationError):
        await tool.execute(value="not-an-int")


@pytest.mark.asyncio
async def test_tool_executor_permissions() -> None:
    """Verifies that ToolExecutor blocks calls lacking correct permissions scopes."""
    tool = DummyTool()
    executor = ToolExecutor([tool])

    # Missing permission scope
    with pytest.raises(PermissionError, match="Lacking required permission"):
        await executor.execute(
            tool_name="dummy_tool",
            arguments={"value": 10},
            caller_permissions=[],
        )

    # Valid permission scope
    res = await executor.execute(
        tool_name="dummy_tool",
        arguments={"value": 10},
        caller_permissions=["admin_scope"],
    )
    assert res == "Result: 10"
