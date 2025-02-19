"""`rest.py` exposes the `Agent` from a REST API.

This module defines a FastAPI app and endpoints that contain
the logic to interact with the `Agent` via HTTP requests.
It also defined a helper function to run the REST API using uvicorn.
"""

import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from rag.agent import Agent

from .models import BaseModel, Messages

app = FastAPI()


class Data(BaseModel):
    """POST input data for the chat endpoint."""

    model: str
    messages: Messages


@app.post("/chat")
async def send_messages(data: Data, stream: bool = False):
    """Receives a POST request with a JSON payload following the `Data` model.

    This function will reject the request if the payload does not conform to the `Data` model.

    Args:
        data (Data): The POST request payload; Must include `model` (str) and `messages` (Messages)
        stream (bool, optional): Query parameter; Whether to return the response as JSON (False) or SSE (True). Defaults to False.

    Returns:
        JSONResponse: If stream is False; A JSON response containing the generated text.
        StreamingResponse: If stream is True; A SSE response containing the generated text in data events.

    """
    agent = Agent(model=data.model)

    response = agent.generate(data.messages.model_dump())

    if stream:

        async def stream_response():
            async for chunk in response:
                yield f"data: {json.dumps(chunk)}\n\n"

        return StreamingResponse(stream_response())
    else:
        buffer = ""

        async for chunk in response:
            buffer += chunk

        return JSONResponse({"response": buffer})


def api():  # pragma: no cover
    """Run the FastAPI app using uvicorn."""
    host = os.environ.get("HOST", "0.0.0.0")
    port = os.environ.get("PORT", "8000")

    uvicorn.run(app, host=host, port=int(port))
