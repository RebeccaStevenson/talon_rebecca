"""Tests for switcher compatibility actions."""

import sys
from types import SimpleNamespace

if "pytest" in sys.modules:
    import user.talon_rebecca.core.app_switcher.switcher_compat  # noqa: F401
    from talon import actions, ui

    def _make_window(app_name: str, title: str, hidden: bool = False):
        return SimpleNamespace(
            app=SimpleNamespace(name=app_name),
            title=title,
            hidden=hidden,
        )

    class TestSwitcherCompat:
        def setup_method(self):
            actions.reset_test_actions()
            ui._windows = []

        def test_focuses_matching_visible_window(self):
            focused = []
            actions.register_test_action(
                "user", "switcher_focus_window", lambda window: focused.append(window)
            )
            match = _make_window("Cursor", "notes.md")
            ui._windows = [
                _make_window("Terminal", "zsh"),
                _make_window("Cursor", "other.md", hidden=True),
                match,
            ]

            actions.user.switcher_focus_app_title("Cursor", "notes")

            assert focused == [match]

        def test_skips_when_no_window_matches(self):
            focused = []
            actions.register_test_action(
                "user", "switcher_focus_window", lambda window: focused.append(window)
            )
            ui._windows = [
                _make_window("Terminal", "zsh"),
                _make_window("Cursor", ""),
            ]

            actions.user.switcher_focus_app_title("*", "notes")

            assert focused == []
