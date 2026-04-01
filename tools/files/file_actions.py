"""
File utility actions for opening paths with the system default handler.
"""
import os
import subprocess

from talon import Module, app

mod = Module()
_IS_MAC = app.platform == "mac"


@mod.action_class
class Actions:
    def open_file_custom(path: str) -> None:
        """Open a file or folder using the system default application."""
        if _IS_MAC:
            subprocess.run(["open", path], check=False)
        else:
            os.startfile(path, "open")  # type: ignore[attr-defined]
