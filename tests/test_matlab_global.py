"""Tests for shared global MATLAB helpers."""

import sys

if "pytest" in sys.modules:
    from talon import actions, app

    import user.talon_rebecca.apps.matlab.matlab_global as matlab_global

    def setup_function():
        actions.reset_test_actions()

    def test_matlab_global_panel_uses_macos_shortcuts(monkeypatch):
        calls = []
        monkeypatch.setattr(app, "platform", "mac")
        actions.register_test_action(
            "user",
            "switcher_focus",
            lambda target: calls.append(("focus", target)),
        )
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))

        actions.user.matlab_global_panel("command")
        actions.user.matlab_global_panel("editor")

        assert calls == [
            ("focus", "matlab"),
            ("key", "cmd-0"),
            ("focus", "matlab"),
            ("key", "cmd-shift-0"),
        ]

    def test_matlab_global_panel_uses_windows_shortcuts(monkeypatch):
        calls = []
        monkeypatch.setattr(app, "platform", "win")
        actions.register_test_action(
            "user",
            "switcher_focus",
            lambda target: calls.append(("focus", target)),
        )
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))

        actions.user.matlab_global_panel("command")
        actions.user.matlab_global_panel("editor")

        assert calls == [
            ("focus", "matlab"),
            ("key", "ctrl-0"),
            ("focus", "matlab"),
            ("key", "ctrl-shift-0"),
        ]

    def test_matlab_global_panel_rejects_unknown_panel():
        try:
            actions.user.matlab_global_panel("workspace")
        except ValueError as exc:
            assert "Unknown MATLAB panel" in str(exc)
        else:
            raise AssertionError("Expected ValueError for unknown MATLAB panel")
