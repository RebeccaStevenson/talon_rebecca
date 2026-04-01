"""Regression tests for custom Google Sheets helpers."""

import sys

if "pytest" in sys.modules:
    import pytest

    import user.talon_rebecca.tools.sheets.sheets as sheets
    from talon import actions, clip

    def setup_function():
        actions.reset_test_actions()
        actions.register_test_action("edit", "copy", lambda: None)
        clip.set_text("")

    def test_get_current_location_parses_single_cell():
        clip.set_text("B12")

        result = sheets.get_current_location()

        assert result.column == "B"
        assert result.row == "12"

    def test_get_current_location_parses_range():
        clip.set_text("A2:B14")

        result = sheets.get_current_location()

        assert result.start.column == "A"
        assert result.start.row == "2"
        assert result.end.column == "B"
        assert result.end.row == "14"

    def test_get_current_location_rejects_unknown_clipboard():
        clip.set_text("not a cell")

        with pytest.raises(ValueError, match="Unknown cell format"):
            sheets.get_current_location()

    def test_select_column_preserves_current_row():
        chrome_mod_calls = []
        inserts = []
        keys = []

        clip.set_text("B12")
        actions.register_test_action(
            "user", "chrome_mod", lambda combo: chrome_mod_calls.append(combo)
        )
        actions.register_test_action("", "insert", lambda text: inserts.append(text))
        actions.register_test_action("", "key", lambda combo: keys.append(combo))

        actions.user.select_column("ZZ")

        assert chrome_mod_calls == ["j"]
        assert inserts == ["ZZ12"]
        assert keys == ["enter"]

    def test_select_row_preserves_current_range_columns():
        chrome_mod_calls = []
        inserts = []
        keys = []

        clip.set_text("A2:B14")
        actions.register_test_action(
            "user", "chrome_mod", lambda combo: chrome_mod_calls.append(combo)
        )
        actions.register_test_action("", "insert", lambda text: inserts.append(text))
        actions.register_test_action("", "key", lambda combo: keys.append(combo))

        actions.user.select_row("7")

        assert chrome_mod_calls == ["j"]
        assert inserts == ["A7:B7"]
        assert keys == ["enter"]
