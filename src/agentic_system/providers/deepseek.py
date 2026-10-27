from collections.abc import Sequence

from ..messages import Message, UserMessage, SystemMessage, AssistantMessage, ToolSpec, ToolCall, ToolResultMessage

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionMessageToolCallParam, ChatCompletionToolParam, ChatCompletionMessageToolCall
import json


class DeepSeekModelClient:
    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model








    def complete(
        self,
        messages: Sequence[Message],
        *,
        tools: Sequence[ToolSpec] = (),
    ) -> AssistantMessage:

        provider_messages: list[ChatCompletionMessageParam] = [
            self._to_provider_message(message) for message in messages
        ]

        provider_tools = [
            self._to_provider_tool_spec(tool_spec) for tool_spec in tools
        ]

        # TODO 2: Make the API request shown above.
        if provider_tools:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=provider_messages,
                tools=provider_tools
            )
        else:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=provider_messages
            )

        # TODO 3: Check that response.choices is not empty.
        # For now, raise ValueError if the provider returned no choices.
        if not response.choices:
            raise ValueError("No choices returned by the provider.")

        # TODO 4: Return our AssistantMessage using the first choice's
        # message.content and an empty tool_calls list.

        
        first_choice_message = response.choices[0].message
        parsed_tool_calls: list[ToolCall] = []

        # TODO: Iterate over first_choice_message.tool_calls or [].
        # Reject a call whose type is not "function" with
        # NotImplementedError.
        # Convert each supported call using self._from_provider_tool_call()
        # and append it to parsed_tool_calls.
        for tool_call in first_choice_message.tool_calls or []:
            if tool_call.type != "function":
                raise NotImplementedError("Unsupported tool call type.")
            parsed_tool_calls.append(self._from_provider_tool_call(tool_call))


        # TODO: If content is None and parsed_tool_calls is empty,
        # raise ValueError: the response contains neither text nor calls.
        if first_choice_message.content is None and not parsed_tool_calls:
            raise ValueError("The response contains neither text nor calls.")

        return AssistantMessage(
            content=first_choice_message.content,
            tool_calls=parsed_tool_calls,
        )



        


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

        if isinstance(message, AssistantMessage):

            if message.tool_calls:

                provider_tool_calls = [self._to_provider_tool_call(tc) for tc in message.tool_calls]

                return {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": provider_tool_calls
                }   

            
            if message.content is None:
                raise ValueError("AssistantMessage must have content.")

            return {
                "role": "assistant",
                "content": message.content
            }


        if isinstance(message, ToolResultMessage):
            return {
                "role": "tool",
                "tool_call_id": message.tool_call_id,
                "content": message.content
            }


        
        raise NotImplementedError("Invalid message type")



    def _from_provider_tool_call(
        self, provider_tool_call: ChatCompletionMessageToolCall
    ) -> ToolCall:

        arguments = json.loads(provider_tool_call.function.arguments)

        if not isinstance(arguments, dict):
            raise ValueError("Tool call arguments must be a dictionary.")

        return ToolCall(
            id=provider_tool_call.id,
            name=provider_tool_call.function.name,
            arguments=arguments
        )
    

    def _to_provider_tool_call(
        self, tool_call: ToolCall
    ) -> ChatCompletionMessageToolCallParam:
        # TODO: Return the structure shown above.
        # Preserve tool_call.id and tool_call.name.
        # Serialize tool_call.arguments using json.dumps().

        return {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.name,
                "arguments": json.dumps(tool_call.arguments, allow_nan=False)
            }
        }


    def _to_provider_tool_spec(
        self, tool_spec: ToolSpec
    ) -> ChatCompletionToolParam:
        # TODO: Return an outer dictionary with:
        # "type": "function"
        # "function": a nested dictionary containing:
        #   "name": tool_spec.name
        #   "description": tool_spec.description
        #   "parameters": tool_spec.input_schema
        
        return {
            "type": "function",
            "function": {
                "name": tool_spec.name,
                "description": tool_spec.description,
                "parameters": tool_spec.input_schema
            }
        }

