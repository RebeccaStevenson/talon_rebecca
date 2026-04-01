"""Declare the shared Zotero app and helper actions."""

from talon import Module, actions, app

mod = Module()

mod.apps.zotero = """
os: mac
and app.bundle: org.zotero.zotero
"""
mod.apps.zotero = r"""
os: windows
and app.name: Zotero
os: windows
and app.exe: /^zotero\.exe$/i
"""


def _zotero_modifier(platform: str | None = None) -> str:
    return "cmd" if (platform or app.platform) == "mac" else "ctrl"


def _zotero_shortcut(suffix: str, platform: str | None = None) -> str:
    separator = "" if suffix.startswith(":") else "-"
    return f"{_zotero_modifier(platform)}{separator}{suffix}"


@mod.action_class
class Actions:
    def zotero_mod(suffix: str):
        """Press a Zotero shortcut with the platform-specific modifier."""
        actions.key(_zotero_shortcut(suffix))
