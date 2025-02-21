"""`types.search` defines the protocol for the search component group.

All components in the search component group must implement this protocol.
This is to ensure external functions can follow this API and be confident
their component will work as expected, regardless of the underlying implementation.
"""

from typing import Any, Protocol, TypedDict

__all__ = ["OptionalSearch", "SearchResult", "SearchResult"]


class SearchResult(TypedDict):
    """Type hinting for a search result."""

    score: float
    data: dict[str, Any]


class Search(Protocol):
    """Protocol for a search component."""

    async def hybrid_search(
        self,
        query: list[float],
        keywords: list[str],
        limit: int = 25,
    ) -> list[SearchResult]:
        """Perform a hybrid search.

        Args:
            query: The query to search for.
            keywords: The keywords to search for.
            limit: The maximum number of results to return.

        Returns:
            A list of search results.
        """
        ...

    async def semantic_search(
        self,
        query: list[float],
        limit: int = 25,
    ) -> list[SearchResult]:
        """Perform a semantic search.

        Args:
            query: The query to search for.
            limit: The maximum number of results to return.

        Returns:
            A list of search results.
        """
        ...

    async def keyword_search(
        self,
        keywords: list[str],
        limit: int = 25,
    ) -> list[SearchResult]:
        """Perform a keyword search.

        Args:
            keywords: The keywords to search for.
            limit: The maximum number of results to return.

        Returns:
            A list of search results.
        """
        ...


type OptionalSearch = Search | None
