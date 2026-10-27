from collections.abc import Mapping

from ..messages import JSONValue, ToolSpec


class EchoTool:
    @property
    def spec(self) -> ToolSpec:
        # TODO: Return a ToolSpec describing the echo tool.
        return ToolSpec(
            name="echo",
            description="Echoes the input text.",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to echo."
                    }
                },
                "required": ["text"],
                "additionalProperties": False
            }
        )
        # raise NotImplementedError("Define the echo tool.")

    def execute(self, arguments: Mapping[str, JSONValue]) -> JSONValue:
        # TODO: Require exactly one argument named "text".
        if "text" not in arguments or len(arguments) != 1:
            raise ValueError("Exactly one argument named 'text' is required.")
        # Reject missing or additional arguments with ValueError.

        text = arguments["text"]
        if not isinstance(text, str):
            raise ValueError("The 'text' argument must be a string.")

        # TODO: Return that string unchanged.
        return text