"""`inference.py` defines the inference component group.

This component group contains components that can run inference on LLM models.

Components:
    OpenAIChat: Run chat completions on OpenAI's models (GPT-family) or with compatible APIs.
"""

from .openai_chat import OpenAIChat

__all__ = ["OpenAIChat"]
