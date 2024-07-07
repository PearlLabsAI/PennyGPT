from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.reactive import reactive
from textual.binding import Binding
from textual.widgets import Input

from ChatMessage import ChatMessage, ChatHistory
from ChatService import ChatService
from UIManager import UIManager
from FileManagerModal import FileManagerModal
from FloatingContextWindow import FloatingContextWindow

import asyncio
import logging


# Set up logging

logging.basicConfig(
    filename="chat.log", level=logging.DEBUG, format="%(levelname)s - %(message)s"
)


class ChatApp(App):
    """Main application class for the chat application."""

    CSS_PATH = "chat.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit the app"),
        Binding("?", "help", "Show help screen"),
        Binding("f", "toggle_file_manager", "Show file manager"),
    ]

    context_files = reactive(set())
    current_response = reactive("")

    def __init__(self):
        super().__init__()
        self.chat_history = ChatHistory()
        self.chat_service = ChatService()
        self.ui_manager = UIManager(self)
        self.response_task = None
        self.sidebar = FloatingContextWindow()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="💬")
        yield self.sidebar
        yield from self.ui_manager.compose()
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.ui_manager.update_chat_display(self.chat_history.messages)

    def action_toggle_file_manager(self) -> None:
        """Show the file manager modal."""
        self.push_screen(FileManagerModal(self.add_file_to_context))

    def add_file_to_context(self, file_path: str) -> None:
        """Add a file to the context for the LLM."""
        logging.debug(f"Attempting to add file: {file_path}")
        if file_path not in self.context_files:
            self.context_files.add(file_path)
            logging.debug(f"Updated context_files: {self.context_files}")
            self.sidebar.update_files(file_path)
            logging.debug("ContextHeader updated")
        else:
            logging.debug(f"File {file_path} already in context")

    def watch_current_response(self, response: str) -> None:
        """Watch for changes in the current response and update the display."""
        self.ui_manager.update_chat_display(self.chat_history.messages, response)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        user_message = event.value
        if user_message:
            self.chat_history.add_message(ChatMessage(user_message, "user"))
            self.ui_manager.update_chat_display(self.chat_history.messages)
            self.ui_manager.clear_input()
            await self.stream_chat_response()

    async def stream_chat_response(self) -> None:
        """Stream the chat response from the API."""
        context = self.get_file_contents()
        self.current_response = ""  # Reset the current response
        async for content in self.chat_service.get_chat_response(
            self.chat_history.to_list(), context
        ):
            self.current_response += content

        self.chat_history.add_message(ChatMessage(self.current_response, "assistant"))
        self.current_response = ""
        self.ui_manager.update_chat_display(self.chat_history.messages)

    def get_file_contents(self) -> str:
        """Get the contents of all context files."""
        contents = []
        logging.debug(f"Getting contents of files: {self.context_files}")
        for file_path in self.context_files:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    contents.append(f"File: {file_path}\n{content}\n")
                    logging.debug(f"Read content from {file_path}")
            except Exception as e:
                error_msg = f"Error reading {file_path}: {str(e)}"
                contents.append(error_msg)
                logging.error(error_msg)
        return "\n".join(contents)

    def action_help(self) -> None:
        """Show the help screen."""
        # Implement your help screen logic here
        pass

    async def on_unmount(self) -> None:
        """Handle cleanup when the app is closing."""
        if self.response_task:
            self.response_task.cancel()
            try:
                await asyncio.wait_for(self.response_task, timeout=1.0)
            except asyncio.TimeoutError:
                pass


if __name__ == "__main__":
    app = ChatApp()
    app.run()
