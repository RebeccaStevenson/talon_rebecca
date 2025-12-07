"""Custom special key mappings for Talon.

Provides explicit bindings so that saying "backspace" removes the character to
the left, while "delete" issues the forward-delete key (removing the character
on the right). Keeping this in the personal `talon_rebecca` set ensures the
behavior persists even after syncing the upstream `community` repo.
"""

from talon import Context

ctx = Context()
ctx.matches = r"""
os: mac
"""

# Core modifier-free keys we want available in command mode.
simple_keys = [
    "end",
    "enter",
    "escape",
    "home",
    "insert",
    "pagedown",
    "pageup",
    "space",
    "tab",
]

# Explicit aliases, focusing on the delete/backspace behavior we care about.
alternate_keys = {
    "backspace": "backspace",        # delete character to the left
    "delete": "delete",              # forward delete (character to the right)
    "forward delete": "delete",
    "page up": "pageup",
    "page down": "pagedown",
}

special_keys = {key: key for key in simple_keys}
special_keys.update(alternate_keys)

ctx.lists["self.special_key"] = special_keys
