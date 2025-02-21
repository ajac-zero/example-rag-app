from rag import config
from rag.components import chat, search, embed


settings = config.Settings()

def test_settings():
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


def test_get_openai_chat():
    openai = config.get_openai_chat()

    assert isinstance(openai, chat.OpenAIChat)

    second_openai = config.get_openai_chat()

    assert openai is second_openai


def test_get_openai_embed():
    openai = config.get_openai_embed()

    assert isinstance(openai, embed.OpenAIEmbed)

    second_openai = config.get_openai_embed()

    assert openai is second_openai
