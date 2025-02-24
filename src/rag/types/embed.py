"""`types.embed` defines the embed protocol."""

from typing import Any, Protocol

__all__ = ["Embed", "OptionalEmbed"]


class Embed(Protocol):
    """Protocol for an embed component."""

    async def generate_embedding(self, text: str, **kwargs: Any) -> list[float]:
        """Generate an embedding from the given text.

        Args:
            text: The text to generate an embedding from.
            model: The model to use for generating the embedding.
            kwargs: Additional keyword arguments to pass to the model.

        Returns:
            An embedding.
        """
        ...


type OptionalEmbed = Embed | None
