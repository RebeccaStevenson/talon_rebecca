"""Tests for app focus and launch helpers."""

import sys
from types import SimpleNamespace

if "pytest" in sys.modules:
    import user.talon_rebecca.core.app_switcher.focus as focus_helpers
    import user.talon_rebecca.system.programs as programs
    import user.talon_rebecca.system.windows_launch as windows_launch
    from talon import actions, app

    class _DummyApp:
        def __init__(self, name: str, title: str):
            self.name = name
            self.active_window = SimpleNamespace(title=title)
            self.focused = False

        def focus(self):
            self.focused = True

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    def test_hierarchical_name_match_prioritizes_match_strategies():
        result = actions.user.heirarchical_name_match(
            "terminal app",
            [
                ("Terminal App", "exact"),
                ("terminal app helper", "prefix"),
                ("best terminal app tool", "substring"),
                ("app random terminal", "fuzzy"),
                ("Terminal App", "exact"),
            ],
            True,
            True,
            True,
        )

        assert result == ["exact", "prefix", "substring", "fuzzy"]

    def test_hierarchical_name_match_is_available_with_correct_spelling():
        result = actions.user.hierarchical_name_match(
            "cursor",
            [("Cursor", "match"), ("Code", "other")],
            True,
            True,
            True,
        )

        assert result == ["match"]

    def test_focus_matches_app_name_and_title(monkeypatch):
        wrong_name = _DummyApp("Notes", "Project Alpha")
        wrong_title = _DummyApp("Cursor", "Scratch Buffer")
        expected = _DummyApp("Cursor", "Project Alpha")
        monkeypatch.setattr(
            programs.ui,
            "apps",
            lambda background=False: [wrong_name, wrong_title, expected],
        )

        actions.user.focus(app_name="cursor", title="project alpha")

        assert expected.focused is True
        assert wrong_name.focused is False
        assert wrong_title.focused is False

    def test_focus_helper_raises_when_focus_fails(monkeypatch):
        broken = _DummyApp("Cursor", "Project Alpha")

        def _focus():
            raise RuntimeError("boom")

        broken.focus = _focus
        monkeypatch.setattr(programs.ui, "apps", lambda background=False: [broken])

        try:
            focus_helpers.focus_running_app(app_name="Cursor")
        except IndexError as error:
            assert 'Problem focussing app: "boom"' == str(error)
        else:
            raise AssertionError("Expected focus_running_app to raise IndexError")

    def test_switch_or_start_launches_then_retries_focus():
        calls = []
        focus_attempts = {"count": 0}

        def _focus(app_name=None, title=None):
            calls.append(("focus", app_name, title))
            focus_attempts["count"] += 1
            if focus_attempts["count"] == 1:
                raise IndexError("missing")

        actions.register_test_action("user", "focus", _focus)
        actions.register_test_action(
            "user",
            "launch_fuzzy",
            lambda program_name: calls.append(("launch", program_name)),
        )
        actions.register_test_action(
            "",
            "sleep",
            lambda duration: calls.append(("sleep", duration)),
        )

        actions.user.switch_or_start("Cursor", focus_title="Workspace", start_delay="3s")

        assert calls == [
            ("focus", None, "Workspace"),
            ("launch", "Cursor"),
            ("sleep", "3s"),
            ("focus", None, "Workspace"),
            ("sleep", "200ms"),
        ]

    def test_open_firefox_uses_keyword_start_delay():
        calls = []
        actions.register_test_action(
            "user",
            "switch_or_start",
            lambda **kwargs: calls.append(kwargs),
        )

        actions.user.open_firefox()

        assert calls == [
            {
                "start_name": "firefox",
                "focus_name": None,
                "focus_title": None,
                "start_delay": "5000ms",
            }
        ]

    def test_focus_talon_repl_uses_console_on_windows(talon_platform):
        calls = []
        talon_platform("windows")
        actions.register_test_action(
            "user",
            "focus",
            lambda app_name=None, title=None: calls.append((app_name, title)),
        )

        actions.user.focus_talon_repl()

        assert calls == [("Console", "Talon REPL")]

    def test_windows_launch_uses_shortcut_match(monkeypatch):
        launched = []
        monkeypatch.setattr(
            windows_launch.ui,
            "launch",
            lambda path=None: (_ for _ in ()).throw(FileNotFoundError()),
        )
        monkeypatch.setattr(windows_launch, "list_appx_packages", lambda: [])
        monkeypatch.setattr(
            windows_launch,
            "_start_menu_shortcuts",
            lambda: [("firefox", "C:/Programs/Firefox.lnk")],
        )
        monkeypatch.setattr(
            windows_launch.os,
            "startfile",
            lambda path: launched.append(path),
            raising=False,
        )

        windows_launch.launch_program_windows("Firefox")

        assert launched == ["C:/Programs/Firefox.lnk"]
