



from ..models import Message, UserMessage, SystemMessage

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

class DeepSeekModelClient:
    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def _to_provider_message(
            self, message: Message
    ) -> ChatCompletionMessageParam:

        if isinstance(message, UserMessage):
            return {
                "role": "user",
                "content": message.content
            }

        
        if isinstance(message, SystemMessage):
            return {
                "role": "system",
                "content": message.content
            }
        raise NotImplementedError("Invalid message type")
