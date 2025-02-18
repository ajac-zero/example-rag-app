from rag.agent import Agent
from rag.types import Messages


async def test_agent(agent: Agent):
    messages: Messages = [{"role": "user", "content": "Hello"}]

    buffer = ""

    async for chunk in agent.generate(messages):
        buffer += chunk

    assert buffer == "Hello, world!"
