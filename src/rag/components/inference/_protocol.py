from typing import Literal, Protocol

from rag.types import AsyncGenerator, Messages, TypedDict

__all__ = ["Function", "StreamPart", "Tool"]


class Function(TypedDict):
    name: str
    arguments: str


class Tool(TypedDict):
    id: str
    type: Literal["function"]
    function: Function


class StreamPart(TypedDict):
    content: str | None
    tools: list[Tool] | None


class InferenceProtocol(Protocol):
    def generate_stream(
        self, messages: Messages, model: str, **kwargs
    ) -> AsyncGenerator[StreamPart, None]: ...

    async def generate_embedding(
        self, text: str, model: str, **kwargs
    ) -> list[float]: ...
