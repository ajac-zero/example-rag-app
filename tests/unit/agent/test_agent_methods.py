async def test_agent(agent):
    messages = [{"role": "user", "content": "Hello"}]

    buffer = ""

    async for chunk in agent.generate(messages):
        buffer += chunk

    assert buffer == "Hello, world!"
