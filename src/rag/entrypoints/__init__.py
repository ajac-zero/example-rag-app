"""`rag.entrypoints` exposes the REST and CLI entrypoints for the application."""

from .cli import app as cli
from .rest import api

__all__ = ["api", "cli"]
