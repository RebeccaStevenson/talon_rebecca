"""Tests for Antigravity helper functions."""

from user.talon_rebecca.apps.antigravity.antigravity_helpers import (
    command_palette_shortcut,
    find_everywhere_shortcut,
    find_shortcut,
    replace_confirm_all_shortcut,
    replace_confirm_shortcut,
    replace_everywhere_shortcut,
    replace_shortcut,
    title_to_filename,
    toggle_match_case_shortcut,
    toggle_match_regex_shortcut,
    toggle_match_word_shortcut,
)


def test_mac_shortcuts():
    assert command_palette_shortcut("mac") == "cmd-shift-p"
    assert find_shortcut("mac") == "cmd-f"
    assert find_everywhere_shortcut("mac") == "cmd-shift-f"
    assert toggle_match_case_shortcut("mac") == "alt-cmd-c"
    assert toggle_match_word_shortcut("mac") == "cmd-alt-w"
    assert toggle_match_regex_shortcut("mac") == "cmd-alt-r"
    assert replace_shortcut("mac") == "alt-cmd-f"
    assert replace_everywhere_shortcut("mac") == "cmd-shift-h"
    assert replace_confirm_shortcut("mac") == "shift-cmd-1"
    assert replace_confirm_all_shortcut("mac") == "cmd-enter"


def test_non_mac_shortcuts():
    assert command_palette_shortcut("windows") == "ctrl-shift-p"
    assert find_shortcut("windows") == "ctrl-f"
    assert find_everywhere_shortcut("windows") == "ctrl-shift-f"
    assert toggle_match_case_shortcut("windows") == "alt-c"
    assert toggle_match_word_shortcut("windows") == "alt-w"
    assert toggle_match_regex_shortcut("windows") == "alt-r"
    assert replace_shortcut("windows") == "ctrl-h"
    assert replace_everywhere_shortcut("windows") == "ctrl-shift-h"
    assert replace_confirm_shortcut("windows") == "ctrl-shift-1"
    assert replace_confirm_all_shortcut("windows") == "ctrl-alt-enter"


def test_title_to_filename_for_mac_titles():
    assert (
        title_to_filename("notes.md — workspace — Antigravity", "mac")
        == "notes.md"
    )


def test_title_to_filename_for_windows_titles():
    assert title_to_filename("notes.md - workspace - Antigravity", "windows") == "notes.md"


def test_title_to_filename_ignores_titles_without_extensions():
    assert title_to_filename("workspace — Antigravity", "mac") == ""
