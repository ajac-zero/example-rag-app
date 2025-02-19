"""`tui.py` contains the terminal user interface for the CLI app.

This module use `rich` to define how the CLI application is rendered in the console.
It does not contain any application logic; It merely determines the style and content
of what is output to the terminal.
"""

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from rag.types import Agent


class ChatUI:  # pragma: no cover
    """The terminal user interface for the CLI app."""

    def __init__(self, agent: Agent):
        """Initialize the ChatUI instance.

        Args:
            agent (Agent): The Agent to use for chatting.

        """
        self.console = Console()
        self.agent = agent

    def print_welcome_message(self) -> None:
        """Print the welcome message to the console."""
        self.console.print(
            "\n[bold cyan]RAG CLI[/]"
            "\nType your messages and press Enter to chat."
            "\nEnter /bye to exit."
        )

    def get_user_input(self, messages: list) -> None:
        """Get user input from the console and append it to the messages list."""
        user_input = self.console.input("\n[bold blue]You:[/]\n")

        if user_input.strip() == "/bye":
            self.console.print("\n[yellow]Exiting chat session...[/]")

            raise SystemExit

        messages.append({"role": "user", "content": user_input})

    async def display_assistant_ouput(self, messages: list) -> None:
        """Display the assistant's output in the console."""
        self.console.print("\n[bold green]Assistant:[/]")

        buffer = ""

        with Live("[grey35]Thinking...[/]", refresh_per_second=10) as live:
            async for content in self.agent.generate(messages):
                buffer += content
                live.update(Markdown(buffer))
