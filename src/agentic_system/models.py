"""Provider-independent message contracts for the agentic system.

Implementation exercise: define the types below using typed dataclasses.
This outline is pseudocode, not an implemented API.

ToolCall:
    id: str
    name: str
    arguments: dict[str, JSONValue]

SystemMessage:
    content: str

UserMessage:
    content: str

AssistantMessage:
    content: str | None
    tool_calls: list[ToolCall]

ToolResultMessage:
    tool_call_id: str
    content: str
    is_error: bool

Message = SystemMessage | UserMessage | AssistantMessage | ToolResultMessage

JSONValue represents null, booleans, numbers, strings, lists of JSON values,
or dictionaries mapping strings to JSON values. It is not unrestricted Any.

Start with ToolCall. Preserve call IDs so results can reference requests.
Keep SDK imports, network calls, and tool execution out of this module.
"""

from typing import TypeAlias
from dataclasses import dataclass



JSONValue: TypeAlias = (
    str | int | float | bool | None
    | list["JSONValue"]
    | dict[str, "JSONValue"]
)


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, JSONValue]


@dataclass
class SystemMessage:
    content: str

@dataclass
class UserMessage:
    content: str

@dataclass
class AssistantMessage:
    content: str | None
    tool_calls: list[ToolCall]

@dataclass
class ToolResultMessage:
    tool_call_id: str
    content: str
    is_error: bool


Message: TypeAlias = (SystemMessage | UserMessage | AssistantMessage | ToolResultMessage)
conversation: list[Message]


if __name__ == "__main__":
    # call = ToolCall(
    #     id="1",
    #     name="echo",
    #     arguments={"text": "hello"}
    # )

    # print(call)

    # conversation = [UserMessage(content="Hello"), AssistantMessage(content="Hi", tool_calls=[])]
    # print(conversation)

    call_one = ToolCall(
        id="call_1",
        name="echo",
        arguments={"text": "hello"}
    )
    print(f"call_one: {call_one}")

    assistant_message = AssistantMessage(
        content=None,
        tool_calls=[call_one]
    )
    print(f"assistant_message: {assistant_message}")

    toolresultmessage = ToolResultMessage(
        tool_call_id="call_1",
        content="hello",
        is_error=False
    )
    print(f"toolresultmessage: {toolresultmessage}")

