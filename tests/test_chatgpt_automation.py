"""Tests for ChatGPT cross-platform shortcut helpers."""

import sys

if "pytest" in sys.modules:
    from talon import actions

    import user.talon_rebecca.apps.chatgpt.chatgpt_automation as chatgpt_automation

    def test_chatgpt_shortcut_uses_cmd_on_mac():
        assert (
            chatgpt_automation._chatgpt_shortcut("shift-o", platform="mac")
            == "cmd-shift-o"
        )

    def test_chatgpt_shortcut_uses_ctrl_on_windows():
        assert (
            chatgpt_automation._chatgpt_shortcut("shift-o", platform="windows")
            == "ctrl-shift-o"
        )

    def test_chatgpt_mod_presses_resolved_shortcut(talon_platform):
        keys = []
        actions.register_test_action("", "key", lambda combo: keys.append(combo))

        talon_platform("windows")
        actions.user.chatgpt_mod("shift-c")

        assert keys == ["ctrl-shift-c"]
