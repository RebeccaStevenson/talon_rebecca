"""Tests for shared audio-device profiles and switch actions."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.system.audio_devices as audio_devices
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    def test_audio_device_name_prefers_private_config(monkeypatch, tmp_path):
        private = tmp_path / "private.json"
        public = tmp_path / "public.json"
        private.write_text('{"system_input_macbook": "Desk Mic"}\n', encoding="utf-8")
        public.write_text('{"system_input_macbook": "Fallback Mic"}\n', encoding="utf-8")
        monkeypatch.setattr(audio_devices, "_PRIVATE_AUDIO_DEVICES_CONFIG", private)
        monkeypatch.setattr(audio_devices, "_PUBLIC_AUDIO_DEVICES_CONFIG", public)

        assert audio_devices.audio_device_name("system_input_macbook") == "Desk Mic"

    def test_system_input_macbook_uses_canonical_device_name():
        calls = []
        actions.register_test_action(
            "user",
            "audio_input_set_preferred",
            lambda device: calls.append(device),
        )

        actions.user.audio_set_system_input_macbook()

        assert calls == ["MacBook Pro Microphone"]

    def test_talon_mic_shokz_notifies_and_sets_microphone():
        mic_calls = []
        notifications = []
        actions.register_test_action(
            "sound",
            "set_microphone",
            lambda device: mic_calls.append(device),
        )
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.audio_set_talon_mic_shokz()

        assert mic_calls == ["Shokz Loop110"]
        assert notifications == [("Talon mic -> Shokz Loop110", "")]

    def test_talon_mic_macbook_quiet_skips_notification():
        mic_calls = []
        notifications = []
        actions.register_test_action(
            "sound",
            "set_microphone",
            lambda device: mic_calls.append(device),
        )
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.audio_set_talon_mic_macbook_quiet()

        assert mic_calls == ["MacBook Pro Microphone"]
        assert notifications == []

    def test_restore_whisper_quiet_restores_without_notification():
        calls = []
        notifications = []
        actions.register_test_action(
            "user",
            "audio_input_restore_saved",
            lambda: calls.append("restore"),
        )
        actions.register_test_action(
            "",
            "sleep",
            lambda duration: calls.append(("sleep", duration)),
        )
        actions.register_test_action(
            "user",
            "whisper_start",
            lambda: calls.append("whisper"),
        )
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.audio_system_input_restore_whisper_quiet()

        assert calls == ["restore", ("sleep", "100ms"), "whisper"]
        assert notifications == []

    def test_audio_set_all_macbook_routes_through_canonical_names():
        calls = []
        notifications = []
        actions.register_test_action(
            "user",
            "audio_input_set_preferred",
            lambda device: calls.append(("input", device)),
        )
        actions.register_test_action(
            "user",
            "audio_output_set_preferred",
            lambda device: calls.append(("output", device)),
        )
        actions.register_test_action(
            "sound",
            "set_microphone",
            lambda device: calls.append(("talon", device)),
        )
        actions.register_test_action(
            "app",
            "notify",
            lambda title="", body="": notifications.append((title, body)),
        )

        actions.user.audio_set_all_macbook()

        assert calls == [
            ("input", "MacBook Pro Microphone"),
            ("talon", "MacBook Pro Microphone"),
            ("output", "MacBook Pro Speakers"),
        ]
        assert notifications == [("All audio -> MacBook Pro", "")]
