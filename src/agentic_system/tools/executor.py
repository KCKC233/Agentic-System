import json
from collections.abc import Mapping

from ..messages import ToolCall, ToolResultMessage
from ..ports import Tool


def execute_tool(
    tool_call: ToolCall,
    tools: Mapping[str, Tool],
) -> ToolResultMessage:
    # TODO: Find the tool using tool_call.name.
    tool = tools.get(tool_call.name)

    # TODO: If absent, return an error ToolResultMessage.
    if tool is None:
        return ToolResultMessage(
            tool_call_id=tool_call.id,
            content=f"Tool '{tool_call.name}' not found.",
            is_error=True
        )

    # TODO: Execute the tool with tool_call.arguments.
    # Catch ValueError from execution and return an error result.
    # Let unexpected exceptions propagate.

    # TODO: Keep string results unchanged.
    # Serialize other results using json.dumps(..., allow_nan=False).

    try:
        result = tool.execute(tool_call.arguments)

    except ValueError as e:
        return ToolResultMessage(
            tool_call_id=tool_call.id,
            content=str(e),
            is_error=True
        )

    if not isinstance(result, str):
        result = json.dumps(result, allow_nan=False)
    return ToolResultMessage(
        tool_call_id=tool_call.id,
        content=result,
        is_error=False
    )