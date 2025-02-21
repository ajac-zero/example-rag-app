async def test_generate_stream(openai_chat):
    buffer = ""

    response = openai_chat.generate_stream(
        messages=[{"role": "user", "content": "Hello"}],
        model="test",
    )

    async for chunk in response:
        assert "content" in chunk
        assert chunk["content"] is not None

        buffer += chunk["content"]

    assert buffer == "Hello, world!"
