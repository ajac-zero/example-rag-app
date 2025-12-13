"""`rag.entrypoints.rest.app` defines the FastAPI application and endpoints.

This module contains the REST API logic that exposes the Agent through HTTP requests.
"""

import json
import os
from collections.abc import AsyncGenerator
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from rag.agent import Rag
from rag.config import settings

from .models import Data

app = FastAPI()


@app.get("/api/models")
async def get_models() -> JSONResponse:
    """Returns a list of available models."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.openai_url}v1/model/info")
        body = response.json()

    model_list = [
        model["model_name"]
        for model in body["data"]
        if model["model_info"]["mode"] == "chat"
    ]
    return JSONResponse({"data": model_list})


@app.post("/api/chat")
async def send_messages(data: Data, stream: bool = False):  # noqa: ANN201
    """Receives a POST request with a JSON payload following the `Data` model.

    This function will reject the request if the payload does not conform to the `Data` model.

    Args:
        data (Data): The POST request payload; Must include `model` (str) and `messages` (Messages)
        stream (bool, optional): Query parameter; Whether to return the response as JSON (False) or SSE (True). Defaults to False.

    Returns:
        JSONResponse: If stream is False; A JSON response containing the generated text.
        StreamingResponse: If stream is True; A SSE response containing the generated text in data events.

    """
    agent = Rag(model=data.model)

    response = agent.generate(data.messages.model_dump())

    if stream:

        async def stream_response() -> AsyncGenerator[str, None]:
            async for chunk in response:
                yield f"data: {json.dumps(chunk)}\n\n"

        return StreamingResponse(stream_response(), media_type="text/event-stream")
    else:
        buffer = ""

        async for chunk in response:
            buffer += chunk

        return JSONResponse({"response": buffer})


if Path("rag-ui/dist").exists():
    static = StaticFiles(directory="rag-ui/dist", html=True)
    app.mount("/", static, name="gui")


def run_api() -> None:  # pragma: no cover
    """Run the FastAPI app using uvicorn."""
    host = os.environ.get("HOST", "127.0.0.1")
    port = os.environ.get("PORT", "8000")

    uvicorn.run(app, host=host, port=int(port))
