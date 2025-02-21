async def test_openai_chat(openai_chat):
    response = openai_chat.generate_stream(
        messages=[{"role": "user", "content": "hello"}],
        model="gpt-3.5-turbo",
        extra_headers={"mock-response": "hi!"},
    )

    buffer = ""

    async for chunk in response:
        assert "content" in chunk
        assert chunk["content"] is not None

        buffer += chunk["content"]

    assert buffer == "hi!"


async def test_openai_chat_tool_call(openai_chat):
    content = "hello"

    response = openai_chat.generate_stream(
        messages=[{"role": "user", "content": content}],
        model="gpt-3.5-turbo",
        extra_headers={
            "mock-response": 'f:{"name":"my_function","arguments":{"first_arg":"one"}}'
        },
    )

    verified = False

    async for chunk in response:
        if (tools := chunk["tools"]) is not None:
            assert len(tools) == 1

            assert tools[0]["function"]["name"] == "my_function"
            assert tools[0]["function"]["arguments"] == '{"first_arg": "one"}'

        verified = True

    if not verified:
        raise AssertionError("No tool call found")
