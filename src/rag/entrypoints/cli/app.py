"""`rag.entrypoints.cli.app` defines the Typer application and CLI commands.

This module contains the CLI logic that exposes the Agent through the console.
"""

import asyncio
from typing import Annotated

from typer import Exit, Option, Typer

from rag.agent import Rag
from rag.types import Messages

from .tui import ChatUI

app = Typer()


@app.command()
def chat(  # pragma: no cover
    model: Annotated[str, Option("-m", "--model", help="The LLM to use")] = "mock",
) -> None:
    """Start an interactive chat session with a RAG LLM."""
    agent = Rag(model=model)

    messages: Messages = [{"role": "system", "content": agent.system}]

    tui = ChatUI(agent=agent)

    async def chat_session() -> None:
        try:
            tui.print_welcome_message()
            while True:
                if messages[-1]["role"] != "tool":
                    tui.get_user_input(messages)
                await tui.display_assistant_output(messages)
        except SystemExit as err:
            raise Exit() from err

    asyncio.run(chat_session())
