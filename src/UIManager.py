from textual.widgets import RichLog, Input, Footer
from textual.containers import Container, Horizontal
from rich.markdown import Markdown
from typing import List
from ChatMessage import ChatMessage


class UIManager:
    """Manages the UI components and updates."""

    def __init__(self, app):
        self.app = app

    def compose(self):
        """Compose the UI elements."""
        yield Container(
            RichLog(id="chat_display", wrap=True),
            Horizontal(
                Input(placeholder="Type your message here...", id="input_field"),
                id="input_container",
            ),
            id="main_container",
        )
        yield Footer()

    def update_chat_display(
        self, messages: List[ChatMessage], current_response: str = ""
    ):
        """Update the chat display with the current messages and ongoing response."""
        chat_display = self.app.query_one("#chat_display", RichLog)
        chat_display.clear()
        for msg in messages:
            role = "User" if msg.role == "user" else "Assistant"
            markdown_content = f"**{role}:** {msg.content}\n\n"
            markdown = Markdown(markdown_content)
            chat_display.write(markdown)

        if current_response:
            markdown_content = f"**Assistant:** {current_response}\n\n"
            markdown = Markdown(markdown_content)
            chat_display.write(markdown)

    def clear_input(self):
        """Clear the input field."""
        input_field = self.app.query_one("#input_field", Input)
        input_field.value = ""

    def focus_input(self):
        """Focus the input field."""
        input_field = self.app.query_one("#input_field", Input)
        input_field.focus()
