import random


async def test_hybrid_search(docs: list[str], qdrant_search):
    result = await qdrant_search.hybrid_search(
        query=[random.uniform(0.0, 1.0) for _ in range(1536)],
        keywords=["dogs", "cats", "cars"],
        limit=3,
    )

    assert len(result) == len(docs)

    datas = [point["data"]["content"] for point in result]

    for doc in docs:
        assert doc in datas


async def test_semantic_search(docs: list[str], qdrant_search):
    result = await qdrant_search.semantic_search(
        query=[random.uniform(0.0, 1.0) for _ in range(1536)],
        limit=3,
    )

    assert len(result) == len(docs)

    datas = [point["data"]["content"] for point in result]

    for doc in docs:
        assert doc in datas


async def test_keyword_search(docs: list[str], qdrant_search):
    result = await qdrant_search.keyword_search(
        keywords=["dog", "book", "car"], limit=3
    )

    assert len(result) == len(docs)

    datas = [point["data"]["content"] for point in result]

    for doc in docs:
        assert doc in datas
