"""Command palette actions for Antigravity."""

from talon import Context, Module, actions, app

from user.talon_rebecca.apps.antigravity.antigravity_helpers import (
    command_palette_shortcut,
)

mod = Module()
ctx = Context()

ctx.matches = r"""
app: antigravity
"""


def execute_command_via_palette(command_id: str, wait: bool = False):
    """Execute a command via the Antigravity command palette."""
    actions.user.antigravity_command_palette()
    actions.insert(command_id)
    actions.key("enter")
    if wait:
        actions.sleep("100ms")


@mod.action_class
class Actions:
    def antigravity(command_id: str):
        """Execute a command via the Antigravity command palette."""
        execute_command_via_palette(command_id)

    def antigravity_and_wait(command_id: str):
        """Execute a command via the Antigravity command palette and wait."""
        execute_command_via_palette(command_id, wait=True)

    def antigravity_terminal(number: int):
        """Activate a terminal by number in Antigravity."""
        actions.user.antigravity(f"workbench.action.terminal.focusAtIndex{number}")

    def antigravity_command_palette():
        """Show the generic command palette shortcut fallback."""
        actions.key("ctrl-shift-p")


@ctx.action_class("user")
class UserActions:
    def antigravity_command_palette():
        actions.key(command_palette_shortcut(app.platform))
