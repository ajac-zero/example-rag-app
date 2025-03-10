import random

import pytest
from fastembed import SparseTextEmbedding
from qdrant_client import models
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.generic import ServerContainer
from testcontainers.qdrant import QdrantContainer

from rag.agent import Agent
from rag.components.chat import OpenAIChat
from rag.components.search import QdrantSearch
from rag.components.embed import OpenAIEmbed


# Constants; These are in a fixture for easy access in other tests
@pytest.fixture(scope="module")
def docs():
    return [
        "My dog's name is Lua. She's named after the programming language of the same name.",
        "The car was a Honda Accord. It was made in Japan.",
        "I was gifted a rare book. It was written by Charles Dickens.",
    ]


# Testcontainers
@pytest.fixture(scope="module")
def mockai():
    with ServerContainer(8100, "ajaczero/mock-ai") as container:
        wait_for_logs(container, "Uvicorn running")
        yield container.get_exposed_port(8100)


@pytest.fixture(scope="module")
def qdrant(docs: list[str]):
    bm25 = SparseTextEmbedding(model_name="Qdrant/bm25")

    embeddings = [[random.uniform(0.0, 1.0) for _ in range(1536)] for _ in docs]
    sparse_embeddings = [next(iter((bm25.query_embed(text)))) for text in docs]

    points = [
        models.PointStruct(
            id=id,
            vector={
                "dense": embedding,
                "sparse": models.SparseVector(
                    indices=sparse_embeddings.indices.astype(float).tolist(),
                    values=sparse_embeddings.values.astype(float).tolist(),
                ),
            },
            payload={"content": doc},
        )
        for id, (doc, embedding, sparse_embeddings) in enumerate(
            zip(docs, embeddings, sparse_embeddings)
        )
    ]

    with QdrantContainer("qdrant/qdrant:latest") as container:
        client = container.get_client()

        client.create_collection(
            collection_name="Wikipedia",
            vectors_config={
                "dense": models.VectorParams(size=1536, distance=models.Distance.COSINE)
            },
            sparse_vectors_config={"sparse": models.SparseVectorParams()},
        )

        client.upsert(collection_name="Wikipedia", points=points)

        yield container.get_exposed_port(6333)


# Clients
@pytest.fixture(scope="function")
def openai_chat(mockai: int):
    return OpenAIChat(
        api_key="mock-api-key", base_url=f"http://localhost:{mockai}/openai"
    )

@pytest.fixture(scope="function")
def openai_embed(mockai: int):
    return OpenAIEmbed(
        model="mock-ada", api_key="mock-api-key", base_url=f"http://localhost:{mockai}/openai"
    )

@pytest.fixture(scope="function")
async def qdrant_search(qdrant: str):
    return QdrantSearch(collection="Wikipedia", url=f"http://localhost:{qdrant}")


# Agent
@pytest.fixture(scope="function")
def agent(qdrant_search: QdrantSearch, openai_chat: OpenAIChat, openai_embed: OpenAIEmbed):
    return Agent(model="mock", _chat=openai_chat, _search=qdrant_search, _embed=openai_embed)
