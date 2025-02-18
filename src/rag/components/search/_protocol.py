"""`search._protocol.py` defines the protocol for the search component group.

All components in the search component group must implement this protocol.
This is to ensure external functions can follow this API and be confident
their component will work as expected, regardless of the underlying implementation.
"""

from typing import Any, Protocol, TypedDict

__all__ = ["SearchResult"]


class SearchResult(TypedDict):
    score: float
    data: dict[str, Any]


class SearchProtocol(Protocol):
    async def hybrid_search(
        self,
        query: list[float],
        keywords: list[str],
        limit: int = 25,
    ) -> list[SearchResult]: ...

    async def semantic_search(
        self,
        query: list[float],
        limit: int = 25,
    ) -> list[SearchResult]: ...

    async def keyword_search(
        self,
        keywords: list[str],
        limit: int = 25,
    ) -> list[SearchResult]: ...
