async def test_semantic_search(qdrant_search):
    result = await qdrant_search.semantic_search(query=[0.1, 0.2, 0.3], limit=3)

    assert result == [
        {"score": 1, "data": {"content": "Dogs are man's best friend"}},
        {"score": 0.5, "data": {"content": "Cats are quite cute"}},
        {"score": 0, "data": {"content": "Cars are a means of transportation"}},
    ]


async def test_keyword_search(qdrant_search):
    result = await qdrant_search.keyword_search(
        keywords=["dogs", "cats", "cars"], limit=3
    )

    assert result == [
        {"score": 1, "data": {"content": "Dogs are man's best friend"}},
        {"score": 0.5, "data": {"content": "Cats are quite cute"}},
        {"score": 0, "data": {"content": "Cars are a means of transportation"}},
    ]


async def test_hybrid_search(qdrant_search):
    result = await qdrant_search.hybrid_search(
        query=[0.1, 0.2, 0.3],
        keywords=["dogs", "cats", "cars"],
        limit=3,
    )

    assert result == [
        {"score": 1, "data": {"content": "Dogs are man's best friend"}},
        {"score": 0.5, "data": {"content": "Cats are quite cute"}},
        {"score": 0, "data": {"content": "Cars are a means of transportation"}},
    ]
