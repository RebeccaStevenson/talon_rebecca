"""Tests for shared agent harness dispatch helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.tools.agents.agents  # noqa: F401
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    def test_agent_cli_insert_slash_uses_harness_specific_mapping():
        inserts = []

        actions.register_test_action("", "insert", lambda text: inserts.append(text))

        actions.user.agent_cli_insert_slash("codex", "resume")
        actions.user.agent_cli_insert_slash("claude", "quit")

        assert inserts == ["/resume", "/exit"]

    def test_agent_slash_command_list_supports_shared_intents():
        inserts = []

        actions.register_test_action("", "insert", lambda text: inserts.append(text))

        actions.user.agent_cli_insert_slash("claude", "compact")
        actions.user.agent_cli_insert_slash("codex", "permissions")

        assert inserts == ["/compact", "/permissions"]

    def test_agent_cli_key_uses_harness_specific_mapping():
        keys = []

        actions.register_test_action("", "key", lambda combo: keys.append(combo))

        actions.user.agent_cli_key("codex", "quit")
        actions.user.agent_cli_key("claude", "cancel")

        assert keys == ["ctrl-c ctrl-c", "ctrl-c"]

    def test_agent_cli_insert_slash_notifies_for_unknown_intent():
        actions.user.agent_cli_insert_slash("codex", "unknown")

        assert app.notifications == [
            ("Agent command unavailable", "Unsupported agent intent: unknown")
        ]
