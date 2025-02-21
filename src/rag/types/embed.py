"""`types.vectorizer` defines the protocol for the vectorizer component group.

All components in the vectorizer component group must implement this protocol.
This is to ensure external functions can follow this API and be confident
their component will work as expected, regardless of the underlying implementation.
"""

from typing import Protocol

__all__ = ["Embed", "OptionalEmbed"]


class Embed(Protocol):
    """Protocol for an embed component."""

    async def generate_embedding(self, text: str, **kwargs) -> list[float]:
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
