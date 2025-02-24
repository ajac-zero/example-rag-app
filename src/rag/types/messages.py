"""`types.messages` defines the types for different messages and message attributes.

Types:
    Messages: A list of arbitrary messages.
    AssistantMessage: A message with role "assistant" and optional tool_calls.
    SystemMessage: A messages with role "system".
    ToolMessage: A message with role "tool".
    Tool: A dict with id, type, and function fields.
    UserMessage: A message with role "user".
"""

from typing import Literal, NotRequired, TypedDict

__all__ = [
    "AssistantMessage",
    "Messages",
    "SystemMessage",
    "Tool",
    "ToolMessage",
    "UserMessage",
]


class AssistantMessage(TypedDict):
    """A message with role "assistant" and optional tool_calls."""

    role: Literal["assistant"]
    content: NotRequired[str]
    tool_calls: NotRequired[list["Tool"]]


class ToolMessage(TypedDict):
    """A message with role "tool" and tool_call_id and content."""

    role: Literal["tool"]
    tool_call_id: str
    content: str


class UserMessage(TypedDict):
    """A message with role "user" and content."""

    role: Literal["user"]
    content: str


class SystemMessage(TypedDict):
    """A message with role "system" and content."""

    role: Literal["system"]
    content: str


type Messages = list[SystemMessage | AssistantMessage | ToolMessage | UserMessage]


class Function(TypedDict):
    name: str
    arguments: str


class Tool(TypedDict):
    """A dict with id, type, and function fields."""

    id: str
    type: Literal["function"]
    function: Function
