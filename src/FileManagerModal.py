from textual.app import ComposeResult
from textual.widgets import DirectoryTree, Footer
from textual.screen import ModalScreen
from textual.binding import Binding


class FileManagerModal(ModalScreen):
    BINDINGS = [
        Binding("enter", "add_selected", "Add Selected"),
        Binding("f", "dismiss", "Close"),
    ]

    def __init__(self, add_file_callback):
        super().__init__()
        self.add_file_callback = add_file_callback
        self.selected_path = None

    def compose(self) -> ComposeResult:
        yield DirectoryTree(".", id="file_tree")
        yield Footer()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.selected_path = event.path

    def action_add_selected(self) -> None:
        if self.selected_path:
            self.add_file_callback(str(self.selected_path))
        else:
            self.dismiss()

    def action_dismiss(self) -> None:
        self.app.pop_screen()
