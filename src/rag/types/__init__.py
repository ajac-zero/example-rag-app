"""`types.py` defines common types used to type hint application code.

This module groups types defined in different modules throught the application.
It only imports these types during development by using the TYPE_CHECKING flag.
At runtime, these types are replaced with dummy `...` constants. Since the types
defined here must only be used in type hints, this subsitution is safe.
This allows us to avoid circular imports at runtime.
"""

from .agent import Agent
from .chat import Chat, OptionalChat, Stream
from .embed import Embed, OptionalEmbed
from .messages import (
    AssistantMessage,
    Messages,
    SystemMessage,
    Tool,
    ToolMessage,
    UserMessage,
)
from .search import OptionalSearch, Search, SearchResult

__all__ = [
    "Agent",
    "AssistantMessage",
    "Chat",
    "Embed",
    "Messages",
    "OptionalChat",
    "OptionalEmbed",
    "OptionalSearch",
    "Search",
    "SearchResult",
    "Stream",
    "SystemMessage",
    "Tool",
    "ToolMessage",
    "UserMessage",
]
