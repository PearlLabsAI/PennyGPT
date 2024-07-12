from textual.app import ComposeResult
from textual.widgets import DirectoryTree, Footer
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.reactive import reactive


class FileManagerModal(ModalScreen):
    context_files = reactive(set())
    BINDINGS = [
        Binding(
            "left", "collapse_directory", "Collapse Directory", priority=True, show=True
        ),
        Binding(
            "right", "expand_directory", "Expand Directory", priority=True, show=True
        ),
        Binding("enter", "add_selected", "Select", priority=True),
        Binding("s", "toggle_select", "Toggle Select"),
        Binding("f", "dismiss", "Close File Manager"),
    ]

    def __init__(self):
        super().__init__()
        self.directory_tree = DirectoryTree(".")

    def compose(self) -> ComposeResult:
        yield self.directory_tree
        yield Footer()

    def on_mount(self):
        self.directory_tree.focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        path = str(event.path)
        if path not in self.context_files:
            self.action_add_file(path)
        else:
            self.action_remove_file(path)
        tree = self.query_one(DirectoryTree)
        tree.refresh()

    def action_add_file(self, path: str) -> None:
        self.context_files.add(path)

    def action_remove_file(self, path: str) -> None:
        self.context_files.remove(path)

    def action_collapse_directory(self) -> None:
        self.query_one(DirectoryTree).action_toggle_node()

    def action_expand_directory(self) -> None:
        self.query_one(DirectoryTree).action_toggle_node()

    def action_dismiss(self) -> None:
        self.dismiss(self.context_files)
