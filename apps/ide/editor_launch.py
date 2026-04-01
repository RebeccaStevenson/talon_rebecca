"""Shared editor launch helpers for Cursor and VS Code."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from talon import actions, app

from user.talon_rebecca.core.platform_utils import (
    expand_path,
    open_path_in_macos_app,
    quote_cli_arg,
)

_IS_MAC = app.platform == "mac"
_POST_LAUNCH_DELAY = "500ms"


@dataclass(frozen=True)
class EditorSpec:
    macos_app_name: str
    windows_candidates: tuple[Path, ...]
    windows_fallback_binary: str
    terminal_command: str
    unavailable_message: str
    focus_callback: Callable[[], None]


def _launch_windows_direct(spec: EditorSpec, target_path: str) -> bool:
    for candidate in spec.windows_candidates:
        if candidate.is_file():
            subprocess.Popen([str(candidate), target_path])
            return True

    try:
        subprocess.Popen([spec.windows_fallback_binary, target_path])
        return True
    except FileNotFoundError:
        return False


def open_editor_workspace(
    spec: EditorSpec,
    path: str,
    *,
    fallback_to_terminal: bool = True,
) -> None:
    """Open a file or directory in the requested editor."""
    target_path = expand_path(path)

    if _IS_MAC:
        launched = open_path_in_macos_app(spec.macos_app_name, target_path)
    else:
        launched = _launch_windows_direct(spec, target_path)

    if launched:
        actions.sleep(_POST_LAUNCH_DELAY)
        spec.focus_callback()
        return

    if fallback_to_terminal:
        command = f"{spec.terminal_command} {quote_cli_arg(target_path, platform=app.platform)}"
        actions.user.run_command_in_new_terminal(
            command,
            post_command_delay="1s",
            close_after=False,
        )
        return

    actions.app.notify(spec.unavailable_message)


def windows_cursor_candidates() -> tuple[Path, ...]:
    """Return likely Cursor executable locations on Windows."""
    return (
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Cursor" / "Cursor.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Cursor" / "Cursor.exe",
        Path(os.environ.get("PROGRAMFILES", "")) / "Cursor" / "Cursor.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Cursor" / "Cursor.exe",
    )


def windows_vscode_candidates() -> tuple[Path, ...]:
    """Return likely VS Code executable locations on Windows."""
    return (
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Programs"
        / "Microsoft VS Code"
        / "Code.exe",
        Path(os.environ.get("PROGRAMFILES", "")) / "Microsoft VS Code" / "Code.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Microsoft VS Code" / "Code.exe",
    )
