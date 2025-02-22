"""`tui.py` contains the terminal user interface for the CLI app.

This module use `rich` to define how the CLI application is rendered in the console.
It does not contain any application logic; It merely determines the style and content
of what is output to the terminal.
"""

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from rag.types import Agent, Messages


class ChatUI:  # pragma: no cover
    """The terminal user interface for the CLI app."""

    def __init__(self, agent: Agent) -> None:
        """Initialize the ChatUI instance.

        Args:
            agent (Agent): The Agent to use for chatting.

        """
        self.console = Console()
        self.agent = agent

    def print_welcome_message(self) -> None:
        """Print the welcome message to the console."""
        self.console.print(
            "\n[bold cyan]RAG CLI[/]\nType your messages and press Enter to chat.\nEnter /bye to exit."
        )

    def get_user_input(self, messages: Messages) -> None:
        """Get user input from the console and append it to the messages list."""
        user_input = self.console.input("\n[bold blue]You:[/]\n")

        if user_input.strip() == "/bye":
            self.console.print("\n[yellow]Exiting chat session...[/]")

            raise SystemExit

        messages.append({"role": "user", "content": user_input})

    async def display_assistant_output(self, messages: Messages) -> None:
        """Display the assistant's output in the console."""
        self.console.print("\n[bold green]Assistant:[/]")

        buffer = ""

        with Live("[grey35]Thinking...[/]", refresh_per_second=10) as live:
            async for content in self.agent.generate(messages):
                buffer += content
                live.update(Markdown(buffer))

            if len(buffer) == 0:
                assistant_messages = [m for m in messages if m["role"] == "assistant"]
                last_assistant_message = assistant_messages[-1]

                if tool_calls := last_assistant_message.get("tool_calls"):
                    for tool_call in tool_calls:
                        name = tool_call["function"]["name"]
                        arguments = tool_call["function"]["arguments"]
                        live.update(
                            f"[bold yellow]Tool call:[/] {name}\n[bold yellow]Arguments:[/] {arguments}"
                        )
