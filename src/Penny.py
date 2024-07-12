from textual.widgets import Footer, Header, DirectoryTree
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.binding import Binding
from textual.widgets import Input
from textual.containers import Grid, Vertical

from ChatMessage import ChatMessage, ChatHistory
from ChatService import ChatService
from ChatDisplay import ChatDisplay
from FloatingContextWindow import FloatingContextWindow


class Penny(App):
    """Main application class for the chat application."""

    CSS_PATH = "chat.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit the app"),
    ]

    context_files = set()
    current_response = reactive("")

    def __init__(self):
        super().__init__()
        self.chat_history = ChatHistory()
        self.chat_service = ChatService()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🪙")
        yield Grid(
            DirectoryTree("."),
            Vertical(
                FloatingContextWindow(disabled=True),
                ChatDisplay(),
                id="main_content",
            ),
            id="app_grid",
        )
        yield Footer()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle file selection in the directory tree."""
        file_path = event.path
        float_context = self.query_one(FloatingContextWindow)
        if file_path in self.context_files:
            self.context_files.remove(file_path)
            float_context.remove_file(file_path)
        else:
            self.context_files.add(file_path)
            float_context.add_file(file_path)

        float_context.refresh()
        self.refresh()

    def action_toggle_file_manager(self) -> None:
        """Toggle the file manager."""
        file_manager = self.query_one(DirectoryTree)
        file_manager.disabled = not file_manager.disabled

    def watch_current_response(self, response: str) -> None:
        """Watch for changes in the current response and update the display."""
        ui_manager = self.query_one(ChatDisplay)
        ui_manager.update_chat_display(self.chat_history.messages, response)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        user_message = event.value
        if user_message:
            self.chat_history.add_message(ChatMessage(user_message, "user"))
            ui_manager = self.query_one(ChatDisplay)
            ui_manager.update_chat_display(self.chat_history.messages)
            ui_manager.clear_input()
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
        ui_manager = self.query_one(ChatDisplay)
        ui_manager.update_chat_display(self.chat_history.messages)

    def get_file_contents(self) -> str:
        """Get the contents of all context files."""
        contents = []
        for file_path in self.context_files:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    contents.append(f"File: {file_path}\n{content}\n")
            except Exception as e:
                error_msg = f"Error reading {file_path}: {str(e)}"
                contents.append(error_msg)
        return "\n".join(contents)


if __name__ == "__main__":
    app = Penny()
    app.run()
