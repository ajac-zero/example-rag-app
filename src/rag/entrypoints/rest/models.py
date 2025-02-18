"""`models.py` defines the Pydantic models used in the REST API.

This module defines models that are used to validate and parse
the JSON payloads sent to the REST API. These models MUST be
respected by the request of they will be rejected.
"""

from typing import Literal

from pydantic import BaseModel, RootModel

__all__ = ["BaseModel", "Messages"]


class Function(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: Function


class AssistantMessage(BaseModel):
    role: Literal["assistant"]
    content: str | None
    tool_calls: list[ToolCall] | None


class ToolMessage(BaseModel):
    role: Literal["tool"]
    tool_call_id: str
    content: str


class UserMessage(BaseModel):
    role: Literal["user"]
    content: str


class Messages(RootModel):
    """Messages represents a list of UserMessage, AssistantMessage, ToolMessage."""

    root: list[AssistantMessage | ToolMessage | UserMessage]
