from pathlib import Path

from talon import Module, actions, app, settings

mod = Module()
mod.list(
    "superwhisper_mode_key",
    desc="SuperWhisper mode key used for deeplinks like superwhisper://mode?key=<key>",
)

mod.setting(
    "superwhisper_record_hotkey",
    type=str,
    default="alt-cmd-r",
    desc="SuperWhisper global hotkey to start/stop recording",
)

mod.setting(
    "superwhisper_mode_hotkey",
    type=str,
    default="alt-cmd-u",
    desc="SuperWhisper global hotkey to toggle mode",
)


def _superwhisper_record_hotkey() -> str:
    return settings.get("user.superwhisper_record_hotkey")


def _superwhisper_mode_hotkey() -> str:
    return settings.get("user.superwhisper_mode_hotkey")


def _superwhisper_open_url(url: str):
    """Open a SuperWhisper deeplink without stealing focus (macOS)."""
    # Using /usr/bin/open avoids shell differences and keeps it predictable.
    actions.user.system_command_nb(f'/usr/bin/open -g "{url}"')


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parent / "scripts"


def _script_path(filename: str) -> Path:
    return _scripts_dir() / filename


@mod.action_class
class Actions:
    # Primary controls
    def whisper_start():
        """Starts Superwhisper and disables Talon speech"""
        actions.key(_superwhisper_record_hotkey())
        actions.speech.disable()

    def whisper_stop(wake_talon: bool = True):
        """Stops Superwhisper and optionally enables Talon speech"""
        actions.key(_superwhisper_record_hotkey())
        if wake_talon:
            actions.speech.enable()

    def whisper_cancel():
        """Cancels Superwhisper and enables Talon speech"""
        actions.speech.enable()
        actions.key("esc")

    def whisper_toggle_mode():
        """Toggles Superwhisper mode"""
        actions.key(_superwhisper_mode_hotkey())

    def whisper_record_mode(mode_key: str):
        """Starts SuperWhisper recording, switches to the specified mode, and disables Talon speech."""
        _superwhisper_open_url("superwhisper://record")
        actions.sleep("100ms")
        _superwhisper_open_url(f"superwhisper://mode?key={mode_key}")
        actions.speech.disable()

    def whisper_set_mode(mode_key: str):
        """Switch SuperWhisper to the specified mode key without starting recording."""
        _superwhisper_open_url(f"superwhisper://mode?key={mode_key}")
        app.notify(f"SuperWhisper mode: {mode_key}")

    # Mode switching
    def whisper_local():
        """Disables speech and switches Superwhisper to local mode"""
        actions.speech.disable()
        actions.user.superwhisper_local_mode()

    def whisper_normal():
        """Enables speech and switches Superwhisper to normal mode"""
        actions.speech.enable()
        actions.user.superwhisper_normal_mode()

    def whisper_super():
        """Disables speech and switches SuperWhisper to super mode (and starts recording if your script does)."""
        actions.speech.disable()
        actions.user.superwhisper_super_mode()

    # Helper functions (called by mode switching)
    def superwhisper_local_mode():
        """Switches Superwhisper to local mode"""
        actions.user.system_command_nb(f'/bin/bash "{_script_path("superwhisper_local_mode.sh")}"')

    # Helper functions (called by mode switching)
    def superwhisper_super_mode():
        """Switches Superwhisper to super mode"""
        actions.user.system_command_nb(f'/bin/bash "{_script_path("superwhisper_super_mode.sh")}"')

    def superwhisper_normal_mode():
        """Switches Superwhisper to normal mode"""
        actions.user.system_command_nb(f'/bin/bash "{_script_path("superwhisper_normal_mode.sh")}"')
