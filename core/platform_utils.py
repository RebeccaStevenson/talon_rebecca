"""Shared platform helpers used across Talon Rebecca modules."""

from __future__ import annotations

import ntpath
import os
import shlex
import subprocess
from pathlib import Path


def expand_path(path: str | Path) -> str:
    """Return an absolute normalized path with ``~`` expanded."""
    return os.path.normpath(os.path.abspath(os.path.expanduser(str(path))))


def command_with_directory(
    command: str,
    path: str | Path | None,
    *,
    os_name: str | None = None,
) -> str:
    """Prefix a shell command with a directory change when a path is provided."""
    if not path:
        return command

    expanded = expand_path(path)
    active_os_name = os_name or os.name
    if active_os_name == "posix":
        return f"cd {shlex.quote(expanded)}\n{command}"

    drive, _ = ntpath.splitdrive(expanded)
    safe_path = expanded.replace('"', '""')
    parts: list[str] = []
    if drive:
        parts.append(drive)
    parts.append(f'cd "{safe_path}"')
    parts.append(command)
    return "\n".join(parts)


def quote_applescript(text: str) -> str:
    """Escape a string for inclusion inside an AppleScript string literal."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def quote_cli_arg(text: str, *, platform: str | None = None) -> str:
    """Quote a CLI argument for the current platform shell."""
    active_platform = platform or ("mac" if os.name == "posix" else "windows")
    if active_platform == "mac":
        return shlex.quote(text)

    safe_text = text.replace('"', '""')
    return f'"{safe_text}"'


def open_path_in_macos_app(
    app_name: str,
    target: str | Path,
    *,
    runner=subprocess.run,
) -> bool:
    """Open a path with a named macOS application."""
    result = runner(["open", "-a", app_name, str(target)], check=False)
    return result.returncode == 0
