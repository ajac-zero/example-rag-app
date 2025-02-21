"""`types.agent` defines the Agent class, which is the main logic abstraction for the application.

The main objective of the Agent class is to provide instructions to the AI through the system prompt and tool definitions,
along with access to components from the 'components' module in order to perform actions as needed.

An Agent instance uses components configured and provided by the 'config' module. It also imports the 'types' module for type-hinting.

The Agent class is what the entrypoints must import to interact with the application logic.
"""

from collections.abc import AsyncGenerator
from typing import Protocol

from .messages import Messages

__all__ = ["Agent"]


class Agent(Protocol):
    """`Agent` encapsulates a system prompt, tool definitions, and tool execution logic."""

    system: str
    tools: list[dict]

    async def execute(self, tool_name: str, *args, **kwargs):
        """Fetch a tool function from the agent's tool map and runs it given the arguments.

        Args:
            tool_name (str): The name of the tool to execute as listed in the agent's tool map.
            *args: Variable-length argument list to pass to the tool function.
            **kwargs: Arbitrary keyword arguments to pass to the tool function.

        Returns:
            The given tool function's return value.

        """
        ...

    def generate(self, messages: Messages, **kwargs) -> AsyncGenerator[str]:
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
