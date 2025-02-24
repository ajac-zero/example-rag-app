"""`types.agent` provides the `Agent` protocol for type annotations."""

from collections.abc import AsyncGenerator
from typing import Any, Protocol

from .messages import Messages

__all__ = ["Agent"]


class Agent(Protocol):
    """`Agent` encapsulates a system prompt, tool definitions, and tool execution logic."""

    system: str
    tools: list[dict]

    async def execute(self, tool_name: str, *args: Any, **kwargs: Any) -> str:
        """Fetch a tool function from the agent's tool map and runs it given the arguments.

        Args:
            tool_name (str): The name of the tool to execute as listed in the agent's tool map.
            *args: Variable-length argument list to pass to the tool function.
            **kwargs: Arbitrary keyword arguments to pass to the tool function.

        Returns:
            The given tool function's return value.

        """
        ...

    def generate(self, messages: Messages, **kwargs: Any) -> AsyncGenerator[str]:
        """Send messages to the LLM to generate a response.

        If the LLM responds with a tool call, execute the tool and
        append the result to the messages list.

        Args:
            messages (Messages): The list of messages to send to the LLM. Each message
                is a dictionary with a "role" key and a "content" key.  The "role" key
                can be "user" or "assistant", and the "content" key is the message
                to send to the LLM.
            **kwargs: Arbitrary keyword arguments to pass to the LLM.

        Returns:
            An asynchronous generator that yields the LLM's response content one token (str) at a time.

        """
        ...
