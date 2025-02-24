"""`components.search` defines the search component group.

This component group contains components that can perform searches on an external knowledge base (VectorDB).

Components:
    QdrantSearch: Perform searches on a Qdrant vector database.
"""

from .qdrant_search import QdrantSearch

__all__ = ["QdrantSearch"]
