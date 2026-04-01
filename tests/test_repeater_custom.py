"""Tests for custom trailing-number repeater behavior."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.plugin.repeater.repeater_custom  # noqa: F401
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    def test_repeat_trailing_number_delegates_to_core_partial_phrase():
        seen = []

        actions.register_test_action(
            "core", "repeat_partial_phrase", lambda times=1: seen.append(times)
        )

        actions.user.repeat_trailing_number(3)

        assert seen == [3]

    def test_repeat_trailing_number_notifies_when_phrase_is_missing():
        def _raise_index_error(_times=1):
            raise IndexError("list index out of range")

        actions.register_test_action("core", "repeat_partial_phrase", _raise_index_error)

        actions.user.repeat_trailing_number(2)

        assert app.notifications == [("Repeat", "No phrase to repeat.")]
