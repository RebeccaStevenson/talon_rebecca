from talon import Module, actions, imgui
from user.talon_rebecca.system.audio_switcher import (
    AudioDeviceController,
    select_from_picker,
    toggle_picker,
)

mod = Module()

OUTPUT_AUDIO_CONTROLLER = AudioDeviceController(
    device_type="output",
    device_label="output",
)

# Cached list for the imgui picker.
_output_device_list: list[str] = []


# ── imgui picker for system audio output ─────────────────────────────
@imgui.open()
def _output_gui(gui: imgui.GUI):
    gui.text("Select System Audio Output")
    gui.line()
    for index, item in enumerate(_output_device_list, 1):
        if gui.button(f"{index}. {item}"):
            actions.user.system_output_select(index)
    gui.spacer()
    if gui.button("Close"):
        actions.user.system_output_selection_hide()


@mod.action_class
class Actions:
    def switch_audio_output():
        """Switch macOS system audio output device using an on-screen menu (requires SwitchAudioSource)."""
        global _output_device_list
        toggle_picker(_output_gui, _output_device_list, OUTPUT_AUDIO_CONTROLLER)

    def system_output_selection_hide():
        """Hide the system audio output selection GUI."""
        _output_gui.hide()

    def system_output_select(index: int):
        """Select a system audio output device by its menu index."""
        select_from_picker(index, _output_device_list, OUTPUT_AUDIO_CONTROLLER, _output_gui)

    def audio_output_set_preferred(device: str):
        """Set macOS system audio output device by best match (requires SwitchAudioSource)."""
        OUTPUT_AUDIO_CONTROLLER.preferred_device(device)
