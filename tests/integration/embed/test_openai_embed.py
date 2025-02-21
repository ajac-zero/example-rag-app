async def test_openai_embed(openai_embed):
    response = await openai_embed.generate_embedding(text="hello")

    assert isinstance(response, list)
    assert isinstance(response[0], float)
    assert len(response) == 1536

