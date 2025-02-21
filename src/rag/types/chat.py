"""`chat.py` defines the chat component group.

This component group contains components that can run chat completions.

Components:
    Chat: Run chat completions on LLM models.
"""

from collections.abc import AsyncGenerator
from typing import Protocol, TypedDict

from .messages import Messages, Tool

__all__ = ["Chat", "OptionalChat", "Stream"]


class StreamPart(TypedDict):
    content: str | None
    tools: list[Tool] | None


type Stream = AsyncGenerator[StreamPart]


class Chat(Protocol):
    """Protocol for an chat component."""

    def generate_stream(self, messages: Messages, model: str, **kwargs) -> Stream:
        """Generate a stream of messages from the given messages.

        Args:
            messages: The messages to generate a stream from.
            model: The model to use for generating the stream.
            kwargs: Additional keyword arguments to pass to the model.

        Yields:
            A stream of messages.
        """
        ...


type OptionalChat = Chat | None
