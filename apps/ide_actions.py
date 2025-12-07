"""
Actions related to launching IDEs and associated utilities.
"""
import os
import subprocess
from pathlib import Path

from talon import Module, actions, app

mod = Module()
_IS_MAC = app.platform == "mac"


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


@mod.action_class
class Actions:
    def open_cursor_workspace(path: str, fallback_to_terminal: bool = True) -> None:
        """Open the provided file or directory in Cursor without relying on a terminal."""
        target_path = os.path.expanduser(path)
        target_path = os.path.normpath(target_path)

        if _IS_MAC:
            result = subprocess.run(
                ["open", "-a", "Cursor", target_path],
                check=False,
            )
            if result.returncode == 0:
                actions.sleep("500ms")
                _focus_cursor()
                return
        else:
            cursor_candidates = [
                Path(os.environ.get("LOCALAPPDATA", ""))
                / "Programs"
                / "Cursor"
                / "Cursor.exe",
                Path(os.environ.get("LOCALAPPDATA", ""))
                / "Cursor"
                / "Cursor.exe",
                Path(os.environ.get("PROGRAMFILES", ""))
                / "Cursor"
                / "Cursor.exe",
                Path(os.environ.get("PROGRAMFILES(X86)", ""))
                / "Cursor"
                / "Cursor.exe",
            ]

            for candidate in cursor_candidates:
                if candidate and candidate.is_file():
                    subprocess.Popen([str(candidate), target_path])
                    actions.sleep("500ms")
                    _focus_cursor()
                    return

            try:
                subprocess.Popen(["cursor.exe", target_path])
                actions.sleep("500ms")
                _focus_cursor()
                return
            except FileNotFoundError:
                pass

        if fallback_to_terminal:
            actions.user.run_command_in_new_terminal(
                f"cursor {path}",
                post_command_delay="1s",
            )
        else:
            actions.app.notify("Unable to locate Cursor application for direct launch.")

    def open_code_workspace(path: str, fallback_to_terminal: bool = True) -> None:
        """Open the provided file or directory in Visual Studio Code without relying on a terminal."""
        target_path = os.path.expanduser(path)
        target_path = os.path.normpath(target_path)

        if _IS_MAC:
            result = subprocess.run(
                ["open", "-a", "Visual Studio Code", target_path],
                check=False,
            )
            if result.returncode == 0:
                actions.sleep("500ms")
                _focus_vscode()
                return
        else:
            code_candidates = [
                Path(os.environ.get("LOCALAPPDATA", ""))
                / "Programs"
                / "Microsoft VS Code"
                / "Code.exe",
                Path(os.environ.get("PROGRAMFILES", ""))
                / "Microsoft VS Code"
                / "Code.exe",
                Path(os.environ.get("PROGRAMFILES(X86)", ""))
                / "Microsoft VS Code"
                / "Code.exe",
            ]

            for candidate in code_candidates:
                if candidate and candidate.is_file():
                    subprocess.Popen([str(candidate), target_path])
                    actions.sleep("500ms")
                    _focus_vscode()
                    return

            try:
                subprocess.Popen(["Code.exe", target_path])
                actions.sleep("500ms")
                _focus_vscode()
                return
            except FileNotFoundError:
                pass

        if fallback_to_terminal:
            safe_path = target_path.replace('"', '\\"') if _IS_MAC else target_path.replace('"', '""')
            command = f'code "{safe_path}"'
            actions.user.run_command_in_new_terminal(
                command,
                post_command_delay="1s",
                close_after=False,
            )
        else:
            actions.app.notify(
                "Unable to locate Visual Studio Code application for direct launch."
            )
