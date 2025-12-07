"""
Cross-platform terminal window utilities and command launchers.
"""
import os
import shlex
import subprocess
from pathlib import Path
from typing import Optional

from talon import Module, actions, app

mod = Module()
_IS_MAC = app.platform == "mac"
_last_windows_terminal_process: Optional[subprocess.Popen] = None


def _command_with_directory(base_command: str, path: Optional[str]) -> str:
    if not path:
        return base_command

    expanded_path = os.path.abspath(os.path.expanduser(path))

    if _IS_MAC:
        return f"cd {shlex.quote(expanded_path)}\n{base_command}"

    drive, _ = os.path.splitdrive(expanded_path)
    safe_path = expanded_path.replace('"', '""')
    commands: list[str] = []
    if drive:
        commands.append(drive)
    commands.append(f'cd "{safe_path}"')
    commands.append(base_command)
    return "\n".join(commands)


@mod.action_class
class Actions:
    def open_new_terminal_window() -> None:
        """Open and focus a new terminal window on the current platform."""
        global _last_windows_terminal_process
        if _IS_MAC:
            actions.user.switcher_focus("terminal")
            actions.sleep("200ms")
            actions.key("cmd-n")
            _last_windows_terminal_process = None
        else:
            wt_path = (
                Path(os.environ.get("LOCALAPPDATA", ""))
                / "Microsoft"
                / "WindowsApps"
                / "wt.exe"
            )
            try:
                if wt_path.exists():
                    _last_windows_terminal_process = subprocess.Popen([str(wt_path)])
                else:
                    _last_windows_terminal_process = subprocess.Popen(["wt.exe"])
            except FileNotFoundError:
                actions.user.open_windows_terminal()
                actions.sleep("200ms")
                actions.key("ctrl-shift-n")
                _last_windows_terminal_process = None
        actions.sleep("600ms")

    def close_terminal_window() -> None:
        """Close the currently focused terminal window."""
        global _last_windows_terminal_process
        if _IS_MAC:
            try:
                actions.user.switcher_focus("terminal")
                actions.sleep("200ms")
                actions.key("cmd-w")
            finally:
                actions.sleep("200ms")
        else:
            if _last_windows_terminal_process is not None:
                try:
                    if _last_windows_terminal_process.poll() is None:
                        _last_windows_terminal_process.terminate()
                except Exception:
                    pass
                finally:
                    _last_windows_terminal_process = None
            actions.sleep("200ms")

    def run_command_in_new_terminal(
        command: str,
        press_enter: bool = True,
        close_after: bool = True,
        post_command_delay: str = "300ms",
    ) -> None:
        """Open a new terminal window, run the command, and optionally close the window."""
        actions.user.open_new_terminal_window()
        actions.sleep("200ms")
        actions.insert(command)
        if press_enter:
            actions.key("enter")
        actions.sleep(post_command_delay)
        if close_after:
            if _IS_MAC:
                actions.user.switcher_focus("terminal")
                actions.sleep("200ms")
            actions.insert("exit")
            actions.key("enter")
            actions.sleep("400ms")
            actions.user.close_terminal_window()

    def launch_codex_cli(path: Optional[str] = None, command_suffix: Optional[str] = None) -> None:
        """Launch Codex CLI in a new terminal, optionally targeting the provided path."""
        command_parts = ["codex"]

        if path:
            expanded_path = os.path.abspath(os.path.expanduser(path))
            if _IS_MAC:
                path_arg = shlex.quote(expanded_path)
            else:
                safe_path = expanded_path.replace('"', '`"')
                path_arg = f'"{safe_path}"'
            command_parts.extend(["--cd", path_arg])

        if command_suffix:
            command_parts.append(command_suffix.strip())

        shell_command = " ".join(command_parts)
        actions.user.run_command_in_new_terminal(
            shell_command, close_after=False, post_command_delay="1s"
        )

    def codex_search(path: Optional[str] = None) -> None:
        """Run Codex search in-place unless a target path is provided."""
        if path:
            actions.user.launch_codex_cli(path, "--search")
        else:
            actions.insert("codex --search")

    def launch_claude_cli(path: Optional[str] = None, command_suffix: Optional[str] = None) -> None:
        """Launch Claude CLI in a new terminal, optionally within the provided path."""
        base_command = "claude"
        if command_suffix:
            base_command = f"{base_command} {command_suffix.strip()}"
        shell_command = _command_with_directory(base_command, path)
        actions.user.run_command_in_new_terminal(
            shell_command, close_after=False, post_command_delay="1s"
        )
