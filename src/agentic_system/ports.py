from typing import Protocol
from collections.abc import Sequence
from .messages import Message, AssistantMessage, ToolSpec





class ModelClient(Protocol):
    def complete(
        self,
        messages: Sequence[Message],
        *,
        tools: Sequence[ToolSpec] = (),
    ) -> AssistantMessage:
        ...