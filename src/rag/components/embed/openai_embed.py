"""`vectorizer._openai.py` defines the OpenAI Vectorizer component.

This component uses the OpenAI API to generate embeddings.
It uses the AsyncOpenAI client to interact with the OpenAI API.
It exposes the following methods:
    - `generate_embedding`: Generates an embedding for a given text.
"""

from typing import Any

from openai import AsyncOpenAI


class OpenAIEmbed:
    """OpenAIEmbed is an embed component that uses the OpenAI API to generate embeddings."""

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str | None = None,
        _openai_client_class: type[AsyncOpenAI] = AsyncOpenAI,
    ) -> None:
        """Initialize an OpenAIInference instance.

        Args:
            model (str): The model to use for embedding generation.
            api_key (str): The API key to use for authentication.
            base_url (str, optional): The base URL of the OpenAI API. Defaults to None.
            _openai_client_class (AsyncOpenAI, optional): The OpenAI client class to use. Defaults to AsyncOpenAI.

        """
        self.model = model
        self.openai = _openai_client_class(api_key=api_key, base_url=base_url)

    async def generate_embedding(self, text: str, **kwargs: Any) -> list[float]:
        """Generate an embedding for a given text.

        Args:
            text (str): The text to generate the embedding for.
            **kwargs: Additional keyword arguments to pass to the OpenAI API.

        Returns:
            list[float]: The embedding vector.

        """
        response = await self.openai.embeddings.create(
            input=text, model=self.model, **kwargs
        )

        embedding = response.data[0].embedding

        return embedding
