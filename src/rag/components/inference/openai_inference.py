"""`openai_inference.py` defines the OpenAIInference component.

This component uses the OpenAI API to generate embeddings and chat completions.
It uses the AsyncOpenAI client to interact with the OpenAI API.
It exposes the following methods:
    - `generate_stream`: Generates a stream of chat completions.
    - `generate_embedding`: Generates an embedding for a given text.
"""

from openai import AsyncOpenAI

from rag.types import AsyncGenerator, Messages, StreamPart, Tool

__all__ = ["OpenAIInference"]


class OpenAIInference:
    """OpenAIInference is a component that uses the OpenAI API to generate embeddings and chat completions."""

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        _openai_client_class=AsyncOpenAI,
    ) -> None:
        """Initialize an OpenAIInference instance.

        Args:
            api_key (str): The API key to use for authentication.
            base_url (str, optional): The base URL of the OpenAI API. Defaults to None.
            _openai_client_class (AsyncOpenAI, optional): The OpenAI client class to use. Defaults to AsyncOpenAI.

        """
        self.openai = _openai_client_class(api_key=api_key, base_url=base_url)

    async def generate_embedding(self, text: str, model: str, **kwargs):
        """Generate an embedding for a given text.

        Args:
            text (str): The text to generate the embedding for.
            model (str): The model to use for the embedding generation.
            **kwargs: Additional keyword arguments to pass to the OpenAI API.

        Returns:
            list[float]: The embedding vector.

        """
        response = await self.openai.embeddings.create(
            input=text, model=model, **kwargs
        )

        embedding = response.data[0].embedding

        return embedding

    async def generate_stream(
        self, messages: Messages, model: str, **kwargs
    ) -> AsyncGenerator[StreamPart, None]:
        """Generate a stream of chat completions.

        Args:
            messages (Iterable[ChatCompletionMessageParam]): The messages to generate the chat completions for.
            model (str): The model to use for the chat completions.
            **kwargs: Additional keyword arguments to pass to the OpenAI API.

        Returns:
            AsyncGenerator[StreamPart, None]: An asynchronous generator that yields the chat completions in chunks.

        """
        response = await self.openai.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            stream=True,
            **kwargs,
        )

        tool_buffer_index: dict[int, Tool] = {}

        async for chunk in response:
            delta = chunk.choices[0].delta
            if content := delta.content:
                yield {"content": content, "tools": None}

            if tool_calls := delta.tool_calls:
                for call in tool_calls:
                    idx = call.index
                    if idx not in tool_buffer_index:
                        tool_buffer_index[idx] = {
                            "id": "",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    if id := call.id:
                        tool_buffer_index[idx]["id"] = id
                    if function := call.function:
                        if name := function.name:
                            tool_buffer_index[idx]["function"]["name"] = name
                        if arguments := function.arguments:
                            tool_buffer_index[idx]["function"]["arguments"] += arguments

        if tool_buffer_index:
            tool_buffers = list(tool_buffer_index.values())
            yield {"content": None, "tools": tool_buffers}
