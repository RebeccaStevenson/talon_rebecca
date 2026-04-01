from talon import Context, actions

ctx = Context()
ctx.matches = r"""
tag: browser
app: Google Chrome
"""


@ctx.action_class("user")
class UserActions:
    def rango_type_hotkey():
        """Press the Chrome-specific Rango request hotkey."""
        actions.key("ctrl-shift-3")
