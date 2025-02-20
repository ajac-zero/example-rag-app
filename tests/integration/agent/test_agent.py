import json

async def test_hybrid_search_pipeline(docs: list[str], agent):
    result = await agent._hybrid_search_pipeline(
        query="My dog's name is Lua.",
        keywords=["dog", "name", "Lua"],
        limit=1,
    )

    formatted_docs = [f"<CONTENT>\n{doc}\n</CONTENT>" for doc in docs]

    assert result in formatted_docs

async def test_semantic_search_pipeline(docs: list[str], agent):
    result = await agent._semantic_search_pipeline(
        query="My dog's name is Lua.",
        limit=1,
    )

    formatted_docs = [f"<CONTENT>\n{doc}\n</CONTENT>" for doc in docs]

    assert result in formatted_docs

async def test_keyword_search_pipeline(docs: list[str], agent):
    result = await agent._keyword_search_pipeline(
        keywords=["dog", "name", "Lua"],
        limit=1,
    )

    formatted_docs = [f"<CONTENT>\n{doc}\n</CONTENT>" for doc in docs]

    assert result in formatted_docs

async def test_execute(docs: list[str], agent):
    result = await agent.execute("keyword_search", keywords=["dog", "name", "Lua"])

    formatted_docs = [f"<CONTENT>\n{doc}\n</CONTENT>" for doc in docs]

    assert result in formatted_docs


async def test_generate(docs: list[str], agent):
    messages = [{"role": "user", "content": "What are the top 5 most similar documents to this one?"}]

    mock_response = {
        "name": "semantic_search",
        "arguments": {"query": "testdoc", "limit": 1},
    }

    extra_headers = {
        "mock-response": f'f:{json.dumps(mock_response)}',
    }

    async for _ in agent.generate(messages, extra_headers=extra_headers): # type: ignore[arg-type]
        continue

    messages.pop()

    assert len(messages) == 3

    formatted_docs = [f"<CONTENT>\n{doc}\n</CONTENT>" for doc in docs]

    assert messages[-1]["content"] in formatted_docs
