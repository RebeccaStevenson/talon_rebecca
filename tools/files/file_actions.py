"""
File utility actions for opening paths with the system default handler.
"""
import os
import subprocess

from talon import Module, app

mod = Module()


def _is_mac() -> bool:
    return app.platform == "mac"


@mod.action_class
class Actions:
    def open_file_custom(path: str) -> None:
        """Open a file or folder using the system default application."""
        if _is_mac():
            subprocess.run(["open", path], check=False)
        else:
            os.startfile(path, "open")  # type: ignore[attr-defined]
