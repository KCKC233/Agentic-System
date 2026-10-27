from typing import Protocol
from collections.abc import Sequence, Mapping
from .messages import JSONValue, Message, AssistantMessage, ToolSpec





class ModelClient(Protocol):
    def complete(
        self,
        messages: Sequence[Message],
        *,
        tools: Sequence[ToolSpec] = (),
    ) -> AssistantMessage:
        ...


class Tool(Protocol):
    @property
    def spec(self) -> ToolSpec:
        ...

    def execute(
        self, arguments: Mapping[str, JSONValue]
    ) -> JSONValue:
        ...