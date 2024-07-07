from textual.app import ComposeResult
from textual.widgets import DirectoryTree, Button
from textual.screen import ModalScreen
from textual.binding import Binding
import logging


class FileManagerModal(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("enter", "add_selected", "Add Selected"),
    ]

    def __init__(self, add_file_callback):
        super().__init__()
        self.add_file_callback = add_file_callback
        self.selected_path = None

    def compose(self) -> ComposeResult:
        yield DirectoryTree(".", id="file_tree")
        yield Button("Add Selected", id="add_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.action_add_selected()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.selected_path = event.path
        logging.debug(f"File selected: {self.selected_path}")

    def action_add_selected(self) -> None:
        if self.selected_path:
            logging.debug(f"Adding file to context: {self.selected_path}")
            self.add_file_callback(str(self.selected_path))
        else:
            logging.debug("No file selected")
        self.dismiss()

    def action_dismiss(self) -> None:
        self.app.pop_screen()
