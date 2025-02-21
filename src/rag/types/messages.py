"""`types.messages` defines the types for messages.

This module defines the types for messages, which are used to communicate between components.

Types:
    AssistantMessage: A type for assistant messages.
    Messages: A type for messages.
    SystemMessage: A type for system messages.
    Tool: A type for tool tools.
    ToolMessage: A type for tool messages.
    UserMessage: A type for user messages.
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
    """AssistantMessage is a type for assistant messages."""

    role: Literal["assistant"]
    content: NotRequired[str]
    tool_calls: NotRequired[list["Tool"]]


class ToolMessage(TypedDict):
    """ToolMessage is a type for tool messages."""

    role: Literal["tool"]
    tool_call_id: str
    content: str


class UserMessage(TypedDict):
    """UserMessage is a type for user messages."""

    role: Literal["user"]
    content: str


class SystemMessage(TypedDict):
    """SystemMessage is a type for system messages."""

    role: Literal["system"]
    content: str


type Messages = list[SystemMessage | AssistantMessage | ToolMessage | UserMessage]


class Function(TypedDict):
    name: str
    arguments: str


class Tool(TypedDict):
    """Tool is a type for tool tools."""

    id: str
    type: Literal["function"]
    function: Function
