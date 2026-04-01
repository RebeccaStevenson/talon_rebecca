"""Tests for shared SwitchAudioSource helpers."""

import sys

if "pytest" in sys.modules:
    import pytest

    import user.talon_rebecca.system.audio_switcher as audio_switcher
    import user.talon_rebecca.system.switch_sound_input as switch_sound_input
    import user.talon_rebecca.system.switch_sound_output as switch_sound_output
    from talon import actions

    class _FakeController:
        def __init__(self, devices=None):
            self.devices = list(devices or [])
            self.saved = False
            self.restored = False
            self.selected = []
            self.preferred = []

        def list_devices(self):
            return list(self.devices)

        def set_device(self, device):
            self.selected.append(device)
            return True

        def save_current_device(self):
            self.saved = True

        def restore_saved_device(self):
            self.restored = True

        def preferred_device(self, device):
            self.preferred.append(device)

    def setup_function():
        actions.reset_test_actions()

    def test_best_device_match_prefers_exact_case_insensitive_then_substring():
        devices = ["MacBook Pro Microphone", "Shokz Loop110", "Loopback Device"]

        assert audio_switcher.best_device_match(devices, "Shokz Loop110") == "Shokz Loop110"
        assert audio_switcher.best_device_match(devices, "shokz loop110") == "Shokz Loop110"
        assert audio_switcher.best_device_match(devices, "loop") == "Shokz Loop110"
        assert audio_switcher.best_device_match(devices, "   ") is None

    def test_list_devices_raises_when_switch_audio_source_missing(monkeypatch):
        monkeypatch.setattr(audio_switcher, "switch_audio_source_path", lambda: None)

        with pytest.raises(audio_switcher.AudioSwitcherError, match="SwitchAudioSource not found"):
            audio_switcher.list_devices("input")

    def test_list_devices_returns_trimmed_lines(monkeypatch):
        monkeypatch.setattr(
            audio_switcher,
            "switch_audio_source_path",
            lambda: "/opt/homebrew/bin/SwitchAudioSource",
        )

        def _fake_run(args, capture_output=False, text=False):
            assert args == [
                "/opt/homebrew/bin/SwitchAudioSource",
                "-a",
                "-t",
                "output",
            ]

            class _Result:
                returncode = 0
                stdout = "Built-in Output\nShokz Loop110\n\n"
                stderr = ""

            return _Result()

        monkeypatch.setattr(audio_switcher.subprocess, "run", _fake_run)

        assert audio_switcher.list_devices("output") == [
            "Built-in Output",
            "Shokz Loop110",
        ]

    def test_get_current_device_returns_first_line(monkeypatch):
        monkeypatch.setattr(
            audio_switcher,
            "switch_audio_source_path",
            lambda: "/opt/homebrew/bin/SwitchAudioSource",
        )

        def _fake_run(args, capture_output=False, text=False):
            assert args == [
                "/opt/homebrew/bin/SwitchAudioSource",
                "-c",
                "-t",
                "input",
            ]

            class _Result:
                returncode = 0
                stdout = "MacBook Pro Microphone\nIgnored second line\n"
                stderr = ""

            return _Result()

        monkeypatch.setattr(audio_switcher.subprocess, "run", _fake_run)

        assert audio_switcher.get_current_device("input") == "MacBook Pro Microphone"

    def test_set_device_raises_with_stderr_when_command_fails(monkeypatch):
        monkeypatch.setattr(
            audio_switcher,
            "switch_audio_source_path",
            lambda: "/opt/homebrew/bin/SwitchAudioSource",
        )

        def _fake_run(args, check=False, capture_output=False, text=False):
            raise audio_switcher.subprocess.CalledProcessError(
                1,
                args,
                stderr="No such device",
            )

        monkeypatch.setattr(audio_switcher.subprocess, "run", _fake_run)

        with pytest.raises(audio_switcher.AudioSwitcherError, match="Failed to set system output: No such device"):
            audio_switcher.set_device("output", "Missing Device")

    def test_audio_device_controller_persists_and_restores_saved_input(tmp_path, monkeypatch):
        notifications = []
        actions.register_test_action("app", "notify", lambda message="": notifications.append(message))

        controller = audio_switcher.AudioDeviceController(
            device_type="input",
            device_label="input",
            saved_device_path=tmp_path / "saved_input.txt",
        )

        monkeypatch.setattr(audio_switcher, "get_current_device", lambda device_type: "MacBook Pro Microphone")
        monkeypatch.setattr(
            audio_switcher,
            "set_device",
            lambda device_type, device: notifications.append((device_type, device)),
        )

        controller.save_current_device()
        controller.restore_saved_device()

        assert (tmp_path / "saved_input.txt").read_text(encoding="utf-8") == "MacBook Pro Microphone\n"
        assert notifications == [
            "Saved input device: MacBook Pro Microphone",
            ("input", "MacBook Pro Microphone"),
            "System input -> MacBook Pro Microphone",
        ]

    def test_audio_device_controller_notifies_when_saved_input_missing(tmp_path):
        notifications = []
        actions.register_test_action("app", "notify", lambda message="": notifications.append(message))

        controller = audio_switcher.AudioDeviceController(
            device_type="input",
            device_label="input",
            saved_device_path=tmp_path / "missing.txt",
        )

        controller.restore_saved_device()

        assert notifications == ["No saved input device (switch first)"]

    def test_audio_device_controller_uses_preferred_match_for_output(monkeypatch):
        notifications = []
        actions.register_test_action("app", "notify", lambda message="": notifications.append(message))

        controller = audio_switcher.AudioDeviceController(
            device_type="output",
            device_label="output",
        )

        monkeypatch.setattr(
            audio_switcher,
            "list_devices",
            lambda device_type: ["Built-in Output", "Shokz Loop110"],
        )
        monkeypatch.setattr(
            audio_switcher,
            "set_device",
            lambda device_type, device: notifications.append((device_type, device)),
        )

        controller.preferred_device("shokz")

        assert notifications == [
            ("output", "Shokz Loop110"),
            "System output -> Shokz Loop110",
        ]

    def test_audio_input_actions_delegate_to_shared_controller(monkeypatch):
        fake_controller = _FakeController()
        monkeypatch.setattr(switch_sound_input, "INPUT_AUDIO_CONTROLLER", fake_controller)

        actions.user.audio_input_save_current()
        actions.user.audio_input_restore_saved()
        actions.user.audio_input_set("Microphone")
        actions.user.audio_input_set_preferred("Preferred")

        assert fake_controller.saved is True
        assert fake_controller.restored is True
        assert fake_controller.selected == ["Microphone"]
        assert fake_controller.preferred == ["Preferred"]

    def test_audio_input_picker_uses_shared_controller(monkeypatch):
        fake_controller = _FakeController(["Mic A", "Mic B"])
        monkeypatch.setattr(switch_sound_input, "INPUT_AUDIO_CONTROLLER", fake_controller)
        switch_sound_input._input_device_list[:] = []
        switch_sound_input._input_gui.hide()

        actions.user.switch_audio_input()

        assert switch_sound_input._input_device_list == ["Mic A", "Mic B"]
        assert switch_sound_input._input_gui.showing is True

        actions.user.system_input_select(2)

        assert fake_controller.selected == ["Mic B"]
        assert switch_sound_input._input_gui.showing is False

    def test_audio_output_picker_uses_shared_controller(monkeypatch):
        fake_controller = _FakeController(["Built-in Output", "Shokz Loop110"])
        monkeypatch.setattr(switch_sound_output, "OUTPUT_AUDIO_CONTROLLER", fake_controller)
        switch_sound_output._output_device_list[:] = []
        switch_sound_output._output_gui.hide()

        actions.user.switch_audio_output()

        assert switch_sound_output._output_device_list == ["Built-in Output", "Shokz Loop110"]
        assert switch_sound_output._output_gui.showing is True

        actions.user.system_output_select(1)

        assert fake_controller.selected == ["Built-in Output"]
        assert switch_sound_output._output_gui.showing is False
