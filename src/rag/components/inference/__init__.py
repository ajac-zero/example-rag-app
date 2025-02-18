"""`inference.py` defines the inference component group.

This component group contains components that can run inference on AI models (LLMS, Embeddings).

Components:
    OpenAIInference: Run inference on OpenAI's models (GPT-family, ADA-family) or with compatible APIs.

"""

from .openai_inference import OpenAIInference

__all__ = ["OpenAIInference"]
