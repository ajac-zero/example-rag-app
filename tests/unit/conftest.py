import pytest
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    Choice,
    ChoiceDelta,
)
from qdrant_client.http.models import QueryResponse, ScoredPoint

from rag.agent import Agent
from rag.components.inference import OpenAIInference
from rag.components.search import QdrantSearch


@pytest.fixture(scope="module")
def openai_inference():
    return OpenAIInference(api_key="", _openai_client_class=FakeAsyncOpenAI)  # type: ignore


@pytest.fixture(scope="module")
def qdrant_search():
    return QdrantSearch(
        collection="test",
        url="",
        api_key="",
        _qdrant_client_class=FakeAsyncQdrantClient,  # type: ignore
    )


@pytest.fixture(scope="module")
def agent(openai_inference: OpenAIInference, qdrant_search: QdrantSearch):
    agent = Agent(model="test")
    agent.inference = openai_inference
    agent.search = qdrant_search
    return agent


class FakeAsyncOpenAI:
    class Response:
        def __init__(self, text: str):
            self.text = list(text)

        def __aiter__(self):
            return self

        async def __anext__(self):
            if len(self.text) > 0:
                content = self.text.pop(0)
                return ChatCompletionChunk(
                    id="0",
                    created=0,
                    model="test",
                    object="chat.completion.chunk",
                    choices=[Choice(index=0, delta=ChoiceDelta(content=content))],
                )
            else:
                raise StopAsyncIteration

    def __init__(self, *args, **kwargs): ...

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    async def create(self, *args, **kwargs):
        return self.Response("Hello, world!")

    @property
    def embeddings(self):
        return self.Embeddings()

    class Embeddings:
        class Response:
            def __init__(self, embedding: list[float]):
                self.data = [self]
                self.embedding = embedding

        async def create(self, *args, **kwargs):
            return self.Response([0.1, 0.2, 0.3])


class FakeAsyncQdrantClient:
    def __init__(self, *args, **kwargs): ...

    async def query_points(self, *args, **kwargs):
        return QueryResponse(
            points=[
                ScoredPoint(
                    id=1,
                    version=0,
                    score=1,
                    payload={"content": "Dogs are man's best friend"},
                ),
                ScoredPoint(
                    id=2,
                    version=0,
                    score=0.5,
                    payload={"content": "Cats are quite cute"},
                ),
                ScoredPoint(
                    id=3,
                    version=0,
                    score=0,
                    payload={"content": "Cars are a means of transportation"},
                ),
            ]
        )
