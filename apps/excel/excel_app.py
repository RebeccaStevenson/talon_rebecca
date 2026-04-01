"""Declare the shared desktop Excel app and helper actions."""

from talon import Module, actions, app

mod = Module()

mod.apps.excel = """
os: mac
and app.bundle: com.microsoft.Excel
"""
mod.apps.excel = r"""
os: windows
and app.name: Microsoft Excel
os: windows
and app.exe: /^excel\.exe$/i
"""


def _excel_modifier(platform: str | None = None) -> str:
    return "cmd" if (platform or app.platform) == "mac" else "ctrl"


def _excel_shortcut(suffix: str, platform: str | None = None) -> str:
    separator = "" if suffix.startswith(":") else "-"
    return f"{_excel_modifier(platform)}{separator}{suffix}"


@mod.action_class
class Actions:
    def excel_mod(suffix: str):
        """Press a desktop Excel shortcut with the platform-specific modifier."""
        actions.key(_excel_shortcut(suffix))

    def excel_desktop_open_goto():
        """Open the desktop Excel go-to dialog."""
        actions.key("ctrl-g")
        actions.sleep("25ms")
        if app.platform == "mac":
            actions.key("tab")

    def excel_desktop_goto_cell_reference(cell_reference: str):
        """Open the desktop Excel go-to dialog and jump to the requested cell."""
        actions.user.excel_desktop_open_goto()
        actions.insert(cell_reference)
        actions.key("enter")
