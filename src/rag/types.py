"""`types.py` defines common types used to type hint application code.

This module groups types defined in different modules throught the application.
It only imports these types during development by using the TYPE_CHECKING flag.
At runtime, these types are replaced with dummy `...` constants. Since the types
defined here must only be used in type hints, this subsitution is safe.
This allows us to avoid circular imports at runtime.
"""

from typing import (
    TYPE_CHECKING,
    AsyncGenerator,
    Iterable,
    Literal,
    NotRequired,
    TypedDict,
)

if TYPE_CHECKING:
    from .agent import Agent
    from .components.inference._protocol import (
        Function,
        InferenceProtocol,
        StreamPart,
        Tool,
    )
    from .components.search._protocol import SearchProtocol, SearchResult


else:
    Agent = ...
    SearchResult = ...
    SearchProtocol = ...
    StreamPart = ...
    Tool = ...
    Function = ...
    InferenceProtocol = ...


class AssistantMessage(TypedDict):
    """Type hinting for an assistant message."""

    role: Literal["assistant"]
    content: NotRequired[str]
    tool_calls: NotRequired[list[Tool]]


class ToolMessage(TypedDict):
    """Type hinting for a tool message."""

    role: Literal["tool"]
    tool_call_id: str
    content: str


class UserMessage(TypedDict):
    """Type hinting for a user message."""

    role: Literal["user"]
    content: str


type Messages = list[AssistantMessage | ToolMessage | UserMessage]

__all__ = [
    "Agent",
    "AssistantMessage",
    "AsyncGenerator",
    "Function",
    "InferenceProtocol",
    "Iterable",
    "Literal",
    "Messages",
    "SearchProtocol",
    "SearchResult",
    "StreamPart",
    "Tool",
    "ToolMessage",
    "UserMessage",
]
