"""`components.embed` defines the embed component group.

This component group contains components that can run inference on LLM models.

Components:
    OpenAIEmbed: Run inference on OpenAI's models (ADA-family) or with compatible APIs.
"""

from .openai_embed import OpenAIEmbed

__all__ = ["OpenAIEmbed"]
