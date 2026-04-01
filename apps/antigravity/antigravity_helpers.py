"""Shared helpers for Antigravity actions."""


def command_palette_shortcut(platform: str) -> str:
    return "cmd-shift-p" if platform == "mac" else "ctrl-shift-p"


def find_shortcut(platform: str) -> str:
    return "cmd-f" if platform == "mac" else "ctrl-f"


def find_everywhere_shortcut(platform: str) -> str:
    return "cmd-shift-f" if platform == "mac" else "ctrl-shift-f"


def toggle_match_case_shortcut(platform: str) -> str:
    return "alt-cmd-c" if platform == "mac" else "alt-c"


def toggle_match_word_shortcut(platform: str) -> str:
    return "cmd-alt-w" if platform == "mac" else "alt-w"


def toggle_match_regex_shortcut(platform: str) -> str:
    return "cmd-alt-r" if platform == "mac" else "alt-r"


def replace_shortcut(platform: str) -> str:
    return "alt-cmd-f" if platform == "mac" else "ctrl-h"


def replace_everywhere_shortcut(platform: str) -> str:
    return "cmd-shift-h" if platform == "mac" else "ctrl-shift-h"


def replace_confirm_shortcut(platform: str) -> str:
    return "shift-cmd-1" if platform == "mac" else "ctrl-shift-1"


def replace_confirm_all_shortcut(platform: str) -> str:
    return "cmd-enter" if platform == "mac" else "ctrl-alt-enter"


def title_to_filename(title: str, platform: str) -> str:
    delimiter = " — " if platform == "mac" else " - "
    result = title.split(delimiter)[0]
    return result if "." in result else ""
