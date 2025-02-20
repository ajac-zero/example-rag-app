"""`cli.py` exposes the `Agent` from a command line interface.

This module defines a Typer app and commands that contain
the logic to interact with the `Agent` via the console.
"""

import asyncio
from typing import Annotated

from typer import Exit, Option, Typer

from rag.agent import Agent

from .tui import ChatUI

app = Typer()


@app.command()
def chat(  # pragma: no cover
    model: Annotated[str, Option("-m", "--model", help="The LLM to use")] = "mock",
):
    """Start an interactive chat session with a RAG LLM."""
    agent = Agent(model=model)

    messages = [{"role": "system", "content": agent.system}]

    tui = ChatUI(agent=agent)

    async def chat_session():
        try:
            tui.print_welcome_message()
            while True:
                tui.get_user_input(messages)
                await tui.display_assistant_output(messages)
        except SystemExit as err:
            raise Exit() from err

    asyncio.run(chat_session())
