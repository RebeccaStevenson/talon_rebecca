"""Tests for voice notification helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.core.voice_notifications as voice_notifications
    from user.talon_rebecca.core.platform_utils import command_with_directory
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()
        voice_notifications._PLAYBACK_PROC = None
        voice_notifications._PLAYBACK_POLL_JOB = None

    def test_validate_script_notifies_when_script_is_missing(tmp_path):
        notifications = []
        voice_notifications.VOICE_SCRIPT_DIR = tmp_path
        voice_notifications.UV_PATH = tmp_path / "uv"
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        assert voice_notifications._validate_script("missing.py") is False
        assert notifications == [("missing.py not found", "")]

    def test_run_voice_script_dispatches_terminal_command(monkeypatch, tmp_path):
        commands = []
        notifications = []
        uv_path = tmp_path / "uv"
        uv_path.write_text("", encoding="utf-8")
        script_dir = tmp_path / "voice"
        script_dir.mkdir()
        (script_dir / "read_text.py").write_text("", encoding="utf-8")
        voice_notifications.UV_PATH = uv_path
        voice_notifications.VOICE_SCRIPT_DIR = script_dir

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, close_after=False, post_command_delay="750ms": commands.append(
                (command, close_after, post_command_delay)
            ),
        )
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        voice_notifications._run_voice_script("read_text.py", "Reading text")

        expected_command = command_with_directory(f"{uv_path} run read_text.py", script_dir)
        assert commands == [(expected_command, False, "750ms")]
        assert notifications == [("Reading text", "")]

    def test_stop_claude_voice_playback_clears_invalid_pid_marker(tmp_path):
        notifications = []
        pid_file = tmp_path / "playback.pid"
        pid_file.write_text("not-a-pid", encoding="utf-8")
        voice_notifications.PLAYBACK_PID_FILE = pid_file
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.stop_claude_voice_playback()

        assert pid_file.exists() is False
        assert notifications == [("Playback PID is invalid; clearing marker", "")]

    def test_read_clipboard_text_aloud_uses_clipboard_contents(monkeypatch):
        calls = []
        monkeypatch.setattr(voice_notifications.clip, "get", lambda: "Read me")
        monkeypatch.setattr(
            voice_notifications,
            "_pipe_text_to_script",
            lambda script_name, text, notify_message: calls.append(
                (script_name, text, notify_message)
            ),
        )

        actions.user.read_clipboard_text_aloud()

        assert calls == [
            ("read_text.py", "Read me", "Reading clipboard text in new terminal")
        ]

    def test_read_text_aloud_rejects_blank_input():
        notifications = []
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.read_text_aloud("   ")

        assert notifications == [("No text to read", "")]

    def test_voice_notifications_config_prefers_private(monkeypatch, tmp_path):
        private = tmp_path / "private.json"
        public = tmp_path / "public.json"
        private.write_text('{"voice_script_dir": "/tmp/private"}\n', encoding="utf-8")
        public.write_text('{"voice_script_dir": "/tmp/public"}\n', encoding="utf-8")
        monkeypatch.setattr(
            voice_notifications,
            "_PRIVATE_VOICE_NOTIFICATIONS_CONFIG",
            private,
        )
        monkeypatch.setattr(
            voice_notifications,
            "_PUBLIC_VOICE_NOTIFICATIONS_CONFIG",
            public,
        )

        config = voice_notifications._voice_notifications_config()

        assert config == {"voice_script_dir": "/tmp/private"}

    def test_configured_int_accepts_string_digits():
        assert voice_notifications._configured_int({"rate": "220"}, "rate") == 220
        assert voice_notifications._configured_int({"rate": "fast"}, "rate") is None
