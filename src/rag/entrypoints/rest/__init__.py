"""`rag.entrypoints.rest` module for REST API functionality."""

from .app import app
from .app import run_api as api

__all__ = ["app", "api"]
