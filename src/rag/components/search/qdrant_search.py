"""`search.qdrant_search` defines the QdrantSearch component.

This component performs searches on a Qdrant vector database.
It uses the QdrantClient to interact with the Qdrant API.
This component exposes the following methods:
    - `hybrid_search`: Performs a hybrid search using BM25 and Qdrant's dense index.
    - `semantic_search`: Performs a semantic search using Qdrant's dense index.
    - `keyword_search`: Performs a keyword search using BM25 and Qdrant's sparse index.
"""

from fastembed import SparseTextEmbedding
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import QueryResponse

from rag.types import SearchResult


class QdrantSearch:
    """QdrantSearch is a component that performs searches on a Qdrant vector database."""

    def __init__(
        self,
        collection: str,
        url: str,
        api_key: str | None = None,
        _dense_index: str = "dense",
        _sparse_index: str = "sparse",
        _qdrant_client_class: type[AsyncQdrantClient] = AsyncQdrantClient,
        _sparse_text_embedding_class: type[SparseTextEmbedding] = SparseTextEmbedding,
    ) -> None:
        """Initialize a QdrantSearch instance.

        Args:
            collection (str): The name of the Qdrant collection to use.
            url (str): The URL of the Qdrant server.
            api_key (str, optional): The API key to use for authentication. Defaults to None.
            _dense_index (str, optional): The name of the dense index to use. Defaults to "dense".
            _sparse_index (str, optional): The name of the sparse index to use. Defaults to "sparse".
            _qdrant_client_class (AsyncQdrantClient, optional): The Qdrant client class to use. Defaults to AsyncQdrantClient.
            _sparse_text_embedding_class (SparseTextEmbedding, optional): The SparseTextEmbedding class to use. Defaults to SparseTextEmbedding.

        """
        self.collection = collection
        self.qdrant = _qdrant_client_class(url, api_key=api_key)
        self.bm25 = _sparse_text_embedding_class(model_name="Qdrant/bm25")
        self.dense_index = _dense_index
        self.sparse_index = _sparse_index

    def _build_result(self, response: QueryResponse) -> list[SearchResult]:
        return [
            {"score": point.score, "data": point.payload}
            for point in response.points
            if point.payload is not None
        ]

    async def hybrid_search(
        self,
        query: list[float],
        keywords: list[str],
        limit: int = 25,
    ) -> list[SearchResult]:
        """Perform a hybrid search using BM25 and Semantic Search.

        Args:
            query (list[float]): The query vector to use for the search.
            keywords (list[str]): The keywords to use for the search.
            limit (int, optional): The maximum number of results to return. Defaults to 25.

        Returns:
            list[SearchResult]: A list of search results, sorted by score.

        """
        text = " ".join(keywords)
        embedding = next(iter(self.bm25.query_embed(text)))

        prefetch = [
            models.Prefetch(query=query, using=self.dense_index, limit=limit),
            models.Prefetch(
                query=models.SparseVector(
                    indices=embedding.indices.astype(float).tolist(),
                    values=embedding.values.astype(float).tolist(),
                ),
                using=self.sparse_index,
                limit=limit,
            ),
        ]

        response = await self.qdrant.query_points(
            self.collection,
            prefetch=prefetch,
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=limit,
        )

        return self._build_result(response)

    async def semantic_search(
        self,
        query: list[float],
        limit: int = 25,
    ) -> list[SearchResult]:
        """Perform a semantic search using Qdrant's dense index.

        Args:
            query (list[float]): The query vector to use for the search.
            limit (int, optional): The maximum number of results to return. Defaults to 25.

        Returns:
            list[SearchResult]: A list of search results, sorted by score.

        """
        response = await self.qdrant.query_points(
            self.collection,
            query=query,
            limit=limit,
            using=self.dense_index,
        )

        return self._build_result(response)

    async def keyword_search(
        self,
        keywords: list[str],
        limit: int = 25,
    ) -> list[SearchResult]:
        """Perform a keyword search using BM25 and Qdrant's sparse index.

        Args:
            keywords (list[str]): The keywords to use for the search.
            limit (int, optional): The maximum number of results to return. Defaults to 25.

        Returns:
            list[SearchResult]: A list of search results, sorted by score.

        """
        text = " ".join(keywords)
        embedding = next(iter(self.bm25.query_embed(text)))

        response = await self.qdrant.query_points(
            self.collection,
            query=models.SparseVector(
                indices=embedding.indices.astype(float).tolist(),
                values=embedding.values.astype(float).tolist(),
            ),
            limit=limit,
            using=self.sparse_index,
        )

        return self._build_result(response)
