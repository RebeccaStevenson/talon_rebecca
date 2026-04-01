"""Tests for IDE launch helpers."""

import sys
from pathlib import Path

if "pytest" in sys.modules:
    import user.talon_rebecca.apps.ide.editor_launch as editor_launch
    import user.talon_rebecca.apps.ide.ide_actions as ide_actions
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    def test_open_cursor_workspace_uses_macos_direct_open(monkeypatch):
        calls = []
        monkeypatch.setattr(editor_launch, "expand_path", lambda path: "/tmp/project")
        monkeypatch.setattr(
            editor_launch,
            "_IS_MAC",
            True,
        )
        monkeypatch.setattr(
            editor_launch,
            "open_path_in_macos_app",
            lambda app_name, target_path: calls.append(("open", app_name, target_path)) or True,
        )
        monkeypatch.setattr(
            ide_actions,
            "_CURSOR_SPEC",
            ide_actions._CURSOR_SPEC.__class__(
                macos_app_name="Cursor",
                windows_candidates=(),
                windows_fallback_binary="cursor.exe",
                terminal_command="cursor",
                unavailable_message="Unable to locate Cursor application for direct launch.",
                focus_callback=lambda: calls.append(("focus", "cursor")),
            ),
        )
        actions.register_test_action(
            "",
            "sleep",
            lambda duration: calls.append(("sleep", duration)),
        )
        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda *args, **kwargs: calls.append(("terminal", args, kwargs)),
        )

        actions.user.open_cursor_workspace("~/project")

        assert calls == [
            ("open", "Cursor", "/tmp/project"),
            ("sleep", "500ms"),
            ("focus", "cursor"),
        ]

    def test_open_code_workspace_falls_back_to_terminal_on_macos(monkeypatch):
        calls = []
        monkeypatch.setattr(editor_launch, "_IS_MAC", True)
        monkeypatch.setattr(
            editor_launch,
            "expand_path",
            lambda path: '/tmp/My "Project"',
        )
        monkeypatch.setattr(
            editor_launch,
            "open_path_in_macos_app",
            lambda *args, **kwargs: False,
        )
        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, post_command_delay="300ms", close_after=True: calls.append(
                (command, post_command_delay, close_after)
            ),
        )

        actions.user.open_code_workspace("~/project")

        assert calls == [("code '/tmp/My \"Project\"'", "1s", False)]

    def test_open_code_workspace_notifies_when_direct_launch_is_unavailable(monkeypatch):
        notifications = []
        monkeypatch.setattr(editor_launch, "_IS_MAC", False)
        monkeypatch.setattr(
            editor_launch,
            "expand_path",
            lambda path: r"C:\Work\Project",
        )

        def _missing_binary(args):
            raise FileNotFoundError

        monkeypatch.setattr(editor_launch.subprocess, "Popen", _missing_binary)
        monkeypatch.setattr(
            editor_launch,
            "windows_vscode_candidates",
            lambda: (),
        )
        monkeypatch.setattr(
            ide_actions,
            "_VSCODE_SPEC",
            ide_actions._VSCODE_SPEC.__class__(
                macos_app_name="Visual Studio Code",
                windows_candidates=(),
                windows_fallback_binary="Code.exe",
                terminal_command="code",
                unavailable_message="Unable to locate Visual Studio Code application for direct launch.",
                focus_callback=ide_actions._VSCODE_SPEC.focus_callback,
            ),
        )
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.open_code_workspace("~/project", fallback_to_terminal=False)

        assert notifications == [
            ("Unable to locate Visual Studio Code application for direct launch.", "")
        ]

    def test_open_cursor_workspace_uses_windows_direct_candidate(monkeypatch):
        calls = []
        fake_binary = Path(r"C:\Cursor\Cursor.exe")
        monkeypatch.setattr(editor_launch, "_IS_MAC", False)
        monkeypatch.setattr(
            editor_launch,
            "expand_path",
            lambda path: r"C:\Work\Project",
        )
        monkeypatch.setattr(
            ide_actions,
            "_CURSOR_SPEC",
            ide_actions._CURSOR_SPEC.__class__(
                macos_app_name="Cursor",
                windows_candidates=(fake_binary,),
                windows_fallback_binary="cursor.exe",
                terminal_command="cursor",
                unavailable_message="Unable to locate Cursor application for direct launch.",
                focus_callback=lambda: calls.append(("focus", "cursor")),
            ),
        )
        monkeypatch.setattr(Path, "is_file", lambda self: self == fake_binary)
        monkeypatch.setattr(
            editor_launch.subprocess,
            "Popen",
            lambda args: calls.append(("popen", args)),
        )
        actions.register_test_action("", "sleep", lambda duration: calls.append(("sleep", duration)))

        actions.user.open_cursor_workspace("~/project")

        assert calls == [
            ("popen", [str(fake_binary), r"C:\Work\Project"]),
            ("sleep", "500ms"),
            ("focus", "cursor"),
        ]
