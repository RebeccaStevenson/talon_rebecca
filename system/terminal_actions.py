"""Cross-platform terminal window utilities and command launchers."""

import os
import shlex
import subprocess
from pathlib import Path
from typing import Optional

from talon import Module, actions, app
from user.talon_rebecca.core.platform_utils import (
    command_with_directory,
    expand_path,
    quote_applescript,
)

mod = Module()
_last_windows_terminal_process: Optional[subprocess.Popen] = None

_AGENT_LAUNCH_SUFFIXES = {
    "default": {
        "codex": None,
        "claude": None,
    },
    # Preserve current local "allow" behavior even though the underlying
    # harnesses expose different permission models.
    "allow": {
        "codex": "--full-auto",
        "claude": "--allow-dangerously-skip-permissions",
    },
    "resume": {
        "codex": "resume",
        "claude": "--resume",
    },
    "yolo": {
        "codex": "--dangerously-bypass-approvals-and-sandbox",
        "claude": "--dangerously-skip-permissions",
    },
}


def _is_mac() -> bool:
    return app.platform == "mac"


def _run_command_via_macos_terminal(command: str) -> bool:
    escaped_command = quote_applescript(command)
    result = subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "Terminal" to activate',
            "-e",
            f'tell application "Terminal" to do script "{escaped_command}"',
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def _normalized_agent(agent: str) -> str:
    normalized = agent.strip().lower()
    if normalized not in ("codex", "claude"):
        raise ValueError(f"Unsupported agent harness: {agent}")
    return normalized


def _normalized_launch_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized not in _AGENT_LAUNCH_SUFFIXES:
        raise ValueError(f"Unsupported agent launch mode: {mode}")
    return normalized


def _looks_like_codex_subcommand(command_suffix: Optional[str]) -> bool:
    if not command_suffix:
        return False
    return not command_suffix.strip().startswith("-")


@mod.action_class
class Actions:
    def open_new_terminal_window() -> None:
        """Open and focus a new terminal window on the current platform."""
        global _last_windows_terminal_process
        if _is_mac():
            try:
                actions.user.switcher_focus("terminal")
                actions.sleep("200ms")
                actions.key("cmd-n")
            except RuntimeError:
                subprocess.Popen(["open", "-a", "Terminal"])
                actions.sleep("1s")
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
        if _is_mac():
            try:
                actions.user.switcher_focus("terminal")
                actions.sleep("200ms")
                actions.key("cmd-w")
            except RuntimeError:
                return
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
        if _is_mac() and press_enter:
            terminal_command = command if not close_after else f"{command}\nexit"
            if _run_command_via_macos_terminal(terminal_command):
                actions.sleep(post_command_delay)
                return

        actions.user.open_new_terminal_window()
        actions.sleep("200ms")
        actions.insert(command)
        if press_enter:
            actions.key("enter")
        actions.sleep(post_command_delay)
        if close_after:
            if _is_mac():
                actions.user.switcher_focus("terminal")
                actions.sleep("200ms")
            actions.insert("exit")
            actions.key("enter")
            actions.sleep("400ms")
            actions.user.close_terminal_window()

    def launch_codex_cli(path: Optional[str] = None, command_suffix: Optional[str] = None) -> None:
        """Launch Codex CLI in a new terminal, optionally targeting the provided path."""
        if path and _looks_like_codex_subcommand(command_suffix):
            base_command = "codex"
            if command_suffix:
                base_command = f"{base_command} {command_suffix.strip()}"
            shell_command = command_with_directory(base_command, path)
            actions.user.run_command_in_new_terminal(
                shell_command, close_after=False, post_command_delay="1s"
            )
            return

        command_parts = ["codex"]

        if path:
            expanded_path = expand_path(path)
            if _is_mac():
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
        shell_command = command_with_directory(base_command, path)
        actions.user.run_command_in_new_terminal(
            shell_command, close_after=False, post_command_delay="1s"
        )

    def agent_cli_launch(
        agent: str,
        path: Optional[str] = None,
        mode: str = "default",
    ) -> None:
        """Launch a supported agent CLI in a new terminal."""
        normalized_agent = _normalized_agent(agent)
        normalized_mode = _normalized_launch_mode(mode)
        command_suffix = _AGENT_LAUNCH_SUFFIXES[normalized_mode][normalized_agent]

        if normalized_agent == "codex":
            actions.user.launch_codex_cli(path, command_suffix)
            return

        actions.user.launch_claude_cli(path, command_suffix)
