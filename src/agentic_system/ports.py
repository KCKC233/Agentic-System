from typing import Protocol
from collections.abc import Sequence
from .models import Message, AssistantMessage





class ModelClient(Protocol):
    def complete(self, messages: Sequence[Message]) -> AssistantMessage:
        ...