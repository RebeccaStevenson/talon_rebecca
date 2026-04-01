"""Actions related to launching IDEs and associated utilities."""

from talon import Module, actions, app
from user.talon_rebecca.apps.ide.editor_launch import (
    EditorSpec,
    open_editor_workspace,
    windows_cursor_candidates,
    windows_vscode_candidates,
)

mod = Module()


def _focus_cursor() -> None:
    """Attempt to focus the Cursor application window."""
    try:
        actions.user.switcher_focus_app_title("Cursor", ".*")
    except Exception:
        pass


def _focus_vscode() -> None:
    """Attempt to focus the Visual Studio Code application window."""
    try:
        actions.user.switcher_focus_app_title("Code", ".*")
    except Exception:
        pass


_CURSOR_SPEC = EditorSpec(
    macos_app_name="Cursor",
    windows_candidates=windows_cursor_candidates(),
    windows_fallback_binary="cursor.exe",
    terminal_command="cursor",
    unavailable_message="Unable to locate Cursor application for direct launch.",
    focus_callback=_focus_cursor,
)

_VSCODE_SPEC = EditorSpec(
    macos_app_name="Visual Studio Code",
    windows_candidates=windows_vscode_candidates(),
    windows_fallback_binary="Code.exe",
    terminal_command="code",
    unavailable_message="Unable to locate Visual Studio Code application for direct launch.",
    focus_callback=_focus_vscode,
)


@mod.action_class
class Actions:
    def open_cursor_workspace(path: str, fallback_to_terminal: bool = True) -> None:
        """Open the provided file or directory in Cursor without relying on a terminal."""
        open_editor_workspace(
            _CURSOR_SPEC,
            path,
            fallback_to_terminal=fallback_to_terminal,
        )

    def open_code_workspace(path: str, fallback_to_terminal: bool = True) -> None:
        """Open the provided file or directory in Visual Studio Code without relying on a terminal."""
        open_editor_workspace(
            _VSCODE_SPEC,
            path,
            fallback_to_terminal=fallback_to_terminal,
        )
