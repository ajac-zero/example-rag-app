async def test_generate_embedding(openai_embed):
    response = await openai_embed.generate_embedding(text="Hello")

    assert isinstance(response, list)
    assert isinstance(response[0], float)
