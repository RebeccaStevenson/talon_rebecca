"""Declare the shared MATLAB app and helper actions."""

from talon import Context, Module, actions, app

mod = Module()
ctx = Context()

mod.apps.matlab = """
os: mac
and app.bundle: com.mathworks.matlab
"""
mod.apps.matlab = r"""
os: windows
and app.name: MATLAB R2019a
os: windows
and app.name: MATLAB R2023b
os: windows
and app.name: MATLAB R2024b
os: windows
and app.exe: /^matlab\.exe$/i
"""

ctx.matches = r"""
app: matlab
"""


def _matlab_modifier(platform: str | None = None) -> str:
    return "cmd" if (platform or app.platform) == "mac" else "ctrl"


def _matlab_shortcut(suffix: str, platform: str | None = None) -> str:
    separator = "" if suffix.startswith(":") else "-"
    return f"{_matlab_modifier(platform)}{separator}{suffix}"


def _matlab_filename(title: str) -> str:
    result = title.rsplit(" - MATLAB", 1)[0]
    result = result.rsplit(" (", 1)[0]
    result = result.rsplit(" •", 1)[0]
    result = result.strip()
    return result if "." in result else ""


@mod.action_class
class Actions:
    def matlab_mod(suffix: str):
        """Press a MATLAB shortcut with the platform-specific modifier."""
        actions.key(_matlab_shortcut(suffix))


@ctx.action_class("edit")
class EditActions:
    def jump_line(n: int):
        actions.user.matlab_mod("shift-0")
        actions.user.matlab_mod("g")
        actions.insert(str(n))
        actions.key("enter")
        actions.sleep("100ms")


@ctx.action_class("user")
class UserActions:
    def find_everywhere(text: str):
        actions.user.matlab_mod("shift-f")
        if text:
            actions.insert(text)

    def replace(text: str):
        actions.key(_matlab_shortcut("alt-f"))
        if text:
            actions.insert(text)

    def replace_everywhere(text: str):
        actions.user.find_everywhere(text)


@ctx.action_class("win")
class WinActions:
    def filename():
        return _matlab_filename(actions.win.title())
