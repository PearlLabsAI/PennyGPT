from textual.widgets import Static
from textual.reactive import reactive
import os
import logging


class FloatingContextWindow(Static):
    context_files = reactive(set())
    visible = reactive(True)
    DEFAULT_CSS = """
    FloatingContextWindow {
        border: solid green;
        padding: 1;
        min-height: 1;
        border-subtitle-align: center;
    }
    """

    def render(self) -> str:
        files = "".join(
            f" * [bold yellow]{os.path.basename(file)}[/bold yellow]"
            for file in self.context_files
        )
        return f"\n{files}"

    def toggle_visibility(self):
        self.visible = not self.visible

    def update_files(self, new_file):
        self.context_files.add(new_file)
        logging.debug(f"Added file to context: {new_file}")
        logging.debug(f"Context files: {self.context_files}")
        self.refresh()

    def watch_context_files(self, context_files):
        if not context_files:
            self.context_files.add("No files in context")
        else:
            try:
                self.context_files.remove("No files in context")
            except KeyError:
                pass
            for file in context_files:
                self.context_files.add(os.path.basename(file))

    def on_mount(self):
        self.watch_context_files(self.context_files)
        self.border_subtitle = "Context"
