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


def _excel_web_shortcut(suffix: str) -> str:
    separator = "" if suffix.startswith(":") else "-"
    return f"ctrl{separator}{suffix}"


def _dialog_select_all_shortcut(platform: str | None = None) -> str:
    return "cmd-a" if (platform or app.platform) == "mac" else "ctrl-a"


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

    def excel_web_mod(suffix: str):
        """Press an Excel for the web shortcut chord."""
        actions.key(_excel_web_shortcut(suffix))

    def excel_web_goto_cell_reference(cell_reference: str):
        """Open the Excel for the web go-to dialog and jump to the requested cell."""
        actions.key("ctrl-g")
        actions.sleep("25ms")
        actions.key(_dialog_select_all_shortcut())
        actions.key("backspace")
        actions.insert(cell_reference)
        actions.key("enter")
