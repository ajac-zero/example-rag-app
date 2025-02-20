async def test_generate_stream(openai_inference):
    buffer = ""

    response = openai_inference.generate_stream(
        messages=[{"role": "user", "content": "Hello"}],
        model="test",
    )

    async for chunk in response:
        assert "content" in chunk
        assert chunk["content"] is not None

        buffer += chunk["content"]

    assert buffer == "Hello, world!"


async def test_generate_embedding(openai_inference):
    response = await openai_inference.generate_embedding(
        text="Hello",
        model="test",
    )

    assert isinstance(response, list)
    assert isinstance(response[0], float)
