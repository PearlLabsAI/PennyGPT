from textual.widgets import RichLog, Input, Footer
from textual.widget import Widget
from textual.containers import Grid
from rich.markdown import Markdown
from typing import List
from ChatMessage import ChatMessage


class ChatDisplay(Widget):
    """Manages the UI components and updates."""

    def __init__(self):
        super().__init__()

    def compose(self):
        """Compose the UI elements."""
        yield Grid(
            RichLog(id="chat_display", wrap=True, highlight=True),
            Input(placeholder="Type your message here...", id="input_field"),
            id="chat_grid",
        )
        yield Footer()

    def update_chat_display(
        self, messages: List[ChatMessage], current_response: str = ""
    ):
        """Update the chat display with the current messages and ongoing response."""
        chat_display = self.query_one("#chat_display", RichLog)
        chat_display.clear()
        for msg in messages:
            role = "User" if msg.role == "user" else "Assistant"
            color = "green" if msg.role == "user" else "blue"
            markdown_content = f"[{color}]{role}: {msg.content}\n\n"
            markdown = Markdown(markdown_content)
            chat_display.write(markdown)

        if current_response:
            markdown_content = f"[red]**Assistant:** {current_response}\n\n[red]"
            markdown = Markdown(markdown_content)
            chat_display.write(markdown)

    def clear_input(self):
        """Clear the input field."""
        input_field = self.query_one("#input_field", Input)
        input_field.value = ""

    def focus_input(self):
        """Focus the input field."""
        input_field = self.query_one("#input_field", Input)
        input_field.focus()
