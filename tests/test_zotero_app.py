"""Tests for Zotero cross-platform helpers."""

import sys

if "pytest" in sys.modules:
    from talon import actions

    import user.talon_rebecca.apps.zotero.zotero_app as zotero_app

    def test_zotero_shortcut_uses_cmd_on_mac():
        assert zotero_app._zotero_shortcut("shift-s", platform="mac") == "cmd-shift-s"

    def test_zotero_shortcut_uses_ctrl_on_windows():
        assert (
            zotero_app._zotero_shortcut("shift-s", platform="windows")
            == "ctrl-shift-s"
        )

    def test_zotero_shortcut_handles_modifier_hold_suffix():
        assert zotero_app._zotero_shortcut(":down", platform="mac") == "cmd:down"

    def test_zotero_mod_presses_resolved_shortcut(talon_platform):
        keys = []
        actions.register_test_action("", "key", lambda combo: keys.append(combo))

        talon_platform("windows")
        actions.user.zotero_mod("tab")

        assert keys == ["ctrl-tab"]
