from textual.widgets import Static
from textual.reactive import reactive
import os


class FloatingContextWindow(Static):
    context_files = set()
    visible = reactive(True)
    DEFAULT_CSS = """
    FloatingContextWindow {
        border: solid green;
        padding: 1;
        border-subtitle-align: center;
        overflow: scroll;
    }
    """

    def render(self) -> str:
        if not self.context_files:
            return "No files in context"

        files = "".join(
            f" * [bold yellow]{os.path.basename(file)}[/bold yellow]"
            for file in self.context_files
        )
        return f"{files}"

    def format_file_list(self):
        if not self.context_files:
            return "No files in context"
        files = "".join(
            f" * [bold yellow]{os.path.basename(file)}[/bold yellow]"
            for file in self.context_files
        )
        return f"\n{files}"

    def add_file(self, new_file):
        self.context_files.add(os.path.basename(new_file))

    def remove_file(self, file):
        self.context_files.remove(os.path.basename(file))
