"""`vectorizer.py` defines the vectorizer component group.

This component group contains components that can run inference on LLM models.

Components:
    OpenAI: Run inference on OpenAI's models (ADA-family) or with compatible APIs.
"""

from .openai_embed import OpenAIEmbed

__all__ = ["OpenAIEmbed"]
