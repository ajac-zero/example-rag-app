import pytest

from rag import config
from rag.components import inference, search


@pytest.fixture(scope="module")
def settings():
    return config.Settings()


def test_settings(settings: config.Settings):
    assert settings.qdrant_collection == "Wikipedia"
    assert str(settings.qdrant_url) == "http://localhost:6333/"
    assert settings.qdrant_api_key is None

    assert str(settings.openai_url) == "http://localhost:4000/"
    assert settings.openai_api_key == "None"


def test_get_qdrant():
    qdrant = config.get_qdrant()

    assert isinstance(qdrant, search.QdrantSearch)

    second_qdrant = config.get_qdrant()

    assert qdrant is second_qdrant


def test_get_openai():
    openai = config.get_openai()

    assert isinstance(openai, inference.OpenAIInference)

    second_openai = config.get_openai()

    assert openai is second_openai
