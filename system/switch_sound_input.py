from pathlib import Path
from talon import Module, actions, imgui
from user.talon_rebecca.system.audio_switcher import (
    AudioDeviceController,
    select_from_picker,
    toggle_picker,
)

mod = Module()

INPUT_AUDIO_CONTROLLER = AudioDeviceController(
    device_type="input",
    device_label="input",
    saved_device_path=Path("/tmp/talon_saved_system_input_device.txt"),
)

# Cached list for the imgui picker.
_input_device_list: list[str] = []


# ── imgui picker for system audio input ──────────────────────────────
@imgui.open()
def _input_gui(gui: imgui.GUI):
    gui.text("Select System Audio Input")
    gui.line()
    for index, item in enumerate(_input_device_list, 1):
        if gui.button(f"{index}. {item}"):
            actions.user.system_input_select(index)
    gui.spacer()
    if gui.button("Close"):
        actions.user.system_input_selection_hide()


@mod.action_class
class Actions:
    def audio_input_save_current():
        """Save the current macOS system input device for later restoration."""
        INPUT_AUDIO_CONTROLLER.save_current_device()

    def audio_input_restore_saved():
        """Restore the previously saved macOS system input device."""
        INPUT_AUDIO_CONTROLLER.restore_saved_device()

    def switch_audio_input():
        """Switch macOS system audio input device using an on-screen menu (requires SwitchAudioSource)."""
        global _input_device_list
        toggle_picker(_input_gui, _input_device_list, INPUT_AUDIO_CONTROLLER)

    def system_input_selection_hide():
        """Hide the system audio input selection GUI."""
        _input_gui.hide()

    def system_input_select(index: int):
        """Select a system audio input device by its menu index."""
        select_from_picker(index, _input_device_list, INPUT_AUDIO_CONTROLLER, _input_gui)

    def audio_input_set(device: str):
        """Set macOS system audio input device by name (requires SwitchAudioSource)."""
        device_name = device.strip()
        if not device_name:
            actions.app.notify("No input device name provided")
            return

        INPUT_AUDIO_CONTROLLER.set_device(device_name)

    def audio_input_set_preferred(device: str):
        """Set macOS system audio input device by best match (requires SwitchAudioSource)."""
        INPUT_AUDIO_CONTROLLER.preferred_device(device)
