"""Tests for desktop Excel cross-platform helpers."""

import sys

if "pytest" in sys.modules:
    from talon import actions

    import user.talon_rebecca.apps.excel.excel_app as excel_app

    def test_excel_shortcut_uses_cmd_on_mac():
        assert excel_app._excel_shortcut("shift-=", platform="mac") == "cmd-shift-="

    def test_excel_shortcut_uses_ctrl_on_windows():
        assert (
            excel_app._excel_shortcut("shift-=", platform="windows")
            == "ctrl-shift-="
        )

    def test_excel_desktop_open_goto_tabs_on_mac(talon_platform):
        calls = []
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))
        actions.register_test_action(
            "", "sleep", lambda duration: calls.append(("sleep", duration))
        )

        talon_platform("mac")
        actions.user.excel_desktop_open_goto()

        assert calls == [
            ("key", "ctrl-g"),
            ("sleep", "25ms"),
            ("key", "tab"),
        ]

    def test_excel_desktop_open_goto_skips_tab_on_windows(talon_platform):
        calls = []
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))
        actions.register_test_action(
            "", "sleep", lambda duration: calls.append(("sleep", duration))
        )

        talon_platform("windows")
        actions.user.excel_desktop_open_goto()

        assert calls == [
            ("key", "ctrl-g"),
            ("sleep", "25ms"),
        ]

    def test_excel_desktop_goto_cell_reference_tabs_on_mac(talon_platform):
        calls = []
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))
        actions.register_test_action(
            "", "sleep", lambda duration: calls.append(("sleep", duration))
        )
        actions.register_test_action(
            "", "insert", lambda text: calls.append(("insert", text))
        )

        talon_platform("mac")
        actions.user.excel_desktop_goto_cell_reference("B12")

        assert calls == [
            ("key", "ctrl-g"),
            ("sleep", "25ms"),
            ("key", "tab"),
            ("insert", "B12"),
            ("key", "enter"),
        ]

    def test_excel_desktop_goto_cell_reference_skips_tab_on_windows(talon_platform):
        calls = []
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))
        actions.register_test_action(
            "", "sleep", lambda duration: calls.append(("sleep", duration))
        )
        actions.register_test_action(
            "", "insert", lambda text: calls.append(("insert", text))
        )

        talon_platform("windows")
        actions.user.excel_desktop_goto_cell_reference("B12")

        assert calls == [
            ("key", "ctrl-g"),
            ("sleep", "25ms"),
            ("insert", "B12"),
            ("key", "enter"),
        ]
