"""Tests for MATLAB cross-platform helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.apps.matlab.matlab_app as matlab_app

    def test_matlab_shortcut_uses_cmd_on_mac():
        assert matlab_app._matlab_shortcut("shift-f", platform="mac") == "cmd-shift-f"

    def test_matlab_shortcut_uses_ctrl_on_windows():
        assert (
            matlab_app._matlab_shortcut("shift-f", platform="windows")
            == "ctrl-shift-f"
        )

    def test_matlab_shortcut_handles_repeat_suffix():
        assert matlab_app._matlab_shortcut("[:7", platform="mac") == "cmd-[:7"

    def test_matlab_filename_parses_editor_title():
        assert (
            matlab_app._matlab_filename("script.m - MATLAB")
            == "script.m"
        )

    def test_matlab_filename_ignores_non_file_titles():
        assert matlab_app._matlab_filename("Command Window - MATLAB") == ""
