"""Tests for compatibility sound actions."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.core.sound_compat as sound_compat
    from talon import actions

    def setup_function():
        actions.reset_test_actions()

    def test_play_ding_uses_expected_sound(monkeypatch):
        calls = []
        monkeypatch.setattr(sound_compat, "_play_sound", lambda name: calls.append(name))

        actions.user.play_ding()

        assert calls == ["play_ding"]

    def test_play_glass_tap_uses_expected_sound(monkeypatch):
        calls = []
        monkeypatch.setattr(sound_compat, "_play_sound", lambda name: calls.append(name))

        actions.user.play_glass_tap()

        assert calls == ["play_glass_tap"]

    def test_play_thunk_uses_expected_sound(monkeypatch):
        calls = []
        monkeypatch.setattr(sound_compat, "_play_sound", lambda name: calls.append(name))

        actions.user.play_thunk()

        assert calls == ["play_thunk"]
