"""`rag.config` configures the application from env variables.

This module configures components based on the attributes of `Settings` and caches them for reuse.
Environment variables are type-checked with pydantic settings to avoid misconfigurations at runtime.

"""

from functools import lru_cache

from pydantic import HttpUrl
from pydantic_settings import BaseSettings

from .components import chat, embed, search

__all__ = ["get_openai_chat", "get_openai_embed", "get_qdrant"]


class Settings(BaseSettings):
    qdrant_collection: str = "Wikipedia"
    qdrant_url: HttpUrl = HttpUrl("http://localhost:6333")
    qdrant_api_key: str | None = None

    openai_embedding_model: str = "text-embedding-3-large"
    openai_url: HttpUrl = HttpUrl("http://localhost:4000")
    openai_api_key: str = "None"


settings = Settings()


@lru_cache(1)
def get_qdrant() -> search.QdrantSearch:
    """Create a QdrantSearch instance from type-checked environment variables. Instance is cached on first call."""
    return search.QdrantSearch(
        collection=settings.qdrant_collection,
        url=str(settings.qdrant_url),
        api_key=settings.qdrant_api_key,
    )


@lru_cache(1)
def get_openai_chat() -> chat.OpenAIChat:
    """Create an OpenAIChat instance from type-checked environment variables. Instance is cached on first call."""
    return chat.OpenAIChat(
        base_url=str(settings.openai_url),
        api_key=settings.openai_api_key,
    )


@lru_cache(1)
def get_openai_embed() -> embed.OpenAIEmbed:
    """Create an OpenAIEmbed instance from type-checked environment variables. Instance is cached on first call."""
    return embed.OpenAIEmbed(
        model=settings.openai_embedding_model,
        base_url=str(settings.openai_url),
        api_key=settings.openai_api_key,
    )
