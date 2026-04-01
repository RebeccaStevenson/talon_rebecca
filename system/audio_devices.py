"""Canonical local audio-device identifiers and shared switch actions."""

from talon import Module, actions

from user.talon_rebecca.core import local_config

mod = Module()

_PRIVATE_AUDIO_DEVICES_CONFIG = local_config.settings_path(
    "audio_devices.json",
    private=True,
)
_PUBLIC_AUDIO_DEVICES_CONFIG = local_config.settings_path(
    "audio_devices.json",
    private=False,
)
_DEFAULT_AUDIO_DEVICES = {
    "system_input_macbook": "MacBook Pro Microphone",
    "system_input_shokz": "Shokz Loop110",
    "talon_mic_macbook": "MacBook Pro Microphone",
    "talon_mic_shokz": "Shokz Loop110",
    "talon_mic_default": "System Default",
    "system_output_macbook": "MacBook Pro Speakers",
    "system_output_shokz": "Shokz Loop110",
    "summary_macbook": "MacBook Pro",
    "summary_shokz": "Shokz Loop110",
}


def audio_devices_config() -> dict:
    """Load optional audio-device overrides from private/public config."""
    return local_config.load_first_json_object(
        (_PRIVATE_AUDIO_DEVICES_CONFIG, _PUBLIC_AUDIO_DEVICES_CONFIG)
    )


def audio_device_name(key: str) -> str:
    """Return the canonical device name for *key*."""
    configured = audio_devices_config().get(key)
    if isinstance(configured, str) and configured.strip():
        return configured.strip()
    return _DEFAULT_AUDIO_DEVICES[key]


def _set_system_input(device_key: str) -> None:
    actions.user.audio_input_set_preferred(audio_device_name(device_key))


def _set_system_output(device_key: str) -> None:
    actions.user.audio_output_set_preferred(audio_device_name(device_key))


def _set_talon_mic(device_key: str, notify_message: str) -> None:
    actions.app.notify(notify_message)
    actions.sound.set_microphone(audio_device_name(device_key))


def _set_talon_mic_quiet(device_key: str) -> None:
    actions.sound.set_microphone(audio_device_name(device_key))


@mod.action_class
class Actions:
    def audio_set_system_input_macbook():
        """Set macOS system input to the canonical MacBook microphone."""
        _set_system_input("system_input_macbook")

    def audio_set_system_input_shokz():
        """Set macOS system input to the canonical Shokz microphone."""
        _set_system_input("system_input_shokz")

    def audio_set_talon_mic_macbook():
        """Set Talon's microphone to the canonical MacBook microphone."""
        _set_talon_mic(
            "talon_mic_macbook",
            f"Talon mic -> {audio_device_name('talon_mic_macbook')}",
        )

    def audio_set_talon_mic_shokz():
        """Set Talon's microphone to the canonical Shokz microphone."""
        _set_talon_mic(
            "talon_mic_shokz",
            f"Talon mic -> {audio_device_name('talon_mic_shokz')}",
        )

    def audio_set_talon_mic_default():
        """Set Talon's microphone back to the canonical default device."""
        _set_talon_mic(
            "talon_mic_default",
            f"Talon mic -> {audio_device_name('talon_mic_default')}",
        )

    def audio_set_talon_mic_macbook_quiet():
        """Set Talon's microphone to the canonical MacBook microphone without notifying."""
        _set_talon_mic_quiet("talon_mic_macbook")

    def audio_set_talon_mic_shokz_quiet():
        """Set Talon's microphone to the canonical Shokz microphone without notifying."""
        _set_talon_mic_quiet("talon_mic_shokz")

    def audio_set_talon_mic_default_quiet():
        """Set Talon's microphone to the canonical default device without notifying."""
        _set_talon_mic_quiet("talon_mic_default")

    def audio_set_system_output_shokz():
        """Set macOS system output to the canonical Shokz output."""
        _set_system_output("system_output_shokz")

    def audio_set_system_output_macbook():
        """Set macOS system output to the canonical MacBook output."""
        _set_system_output("system_output_macbook")

    def audio_system_input_macbook_whisper():
        """Set system input to MacBook, then start SuperWhisper."""
        app_label = audio_device_name("summary_macbook")
        actions.app.notify(f"System mic -> {app_label} + SuperWhisper")
        actions.user.audio_input_save_current()
        _set_system_input("system_input_macbook")
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_system_input_restore_whisper():
        """Restore saved system input, then start SuperWhisper."""
        actions.app.notify("System mic -> restore saved + SuperWhisper")
        actions.user.audio_input_restore_saved()
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_talon_mic_macbook_whisper():
        """Set Talon's mic to MacBook, then start SuperWhisper."""
        app_label = audio_device_name("summary_macbook")
        actions.app.notify(f"Talon mic -> {app_label} + SuperWhisper")
        actions.sound.set_microphone(audio_device_name("talon_mic_macbook"))
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_talon_mic_default_whisper():
        """Set Talon's mic to default, then start SuperWhisper."""
        actions.app.notify(
            f"Talon mic -> {audio_device_name('talon_mic_default')} + SuperWhisper"
        )
        actions.sound.set_microphone(audio_device_name("talon_mic_default"))
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_system_input_macbook_whisper_quiet():
        """Set system input to MacBook, then start SuperWhisper without summary notification."""
        actions.user.audio_input_save_current()
        _set_system_input("system_input_macbook")
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_system_input_restore_whisper_quiet():
        """Restore saved system input, then start SuperWhisper without summary notification."""
        actions.user.audio_input_restore_saved()
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_talon_mic_macbook_whisper_quiet():
        """Set Talon's mic to MacBook, then start SuperWhisper without notification."""
        actions.sound.set_microphone(audio_device_name("talon_mic_macbook"))
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_talon_mic_default_whisper_quiet():
        """Set Talon's mic to default, then start SuperWhisper without notification."""
        actions.sound.set_microphone(audio_device_name("talon_mic_default"))
        actions.sleep("100ms")
        actions.user.whisper_start()

    def audio_set_all_shokz():
        """Set system input, Talon mic, and output to the Shokz profile."""
        actions.app.notify(f"All audio -> {audio_device_name('summary_shokz')}")
        _set_system_input("system_input_shokz")
        actions.sound.set_microphone(audio_device_name("talon_mic_shokz"))
        _set_system_output("system_output_shokz")

    def audio_set_all_macbook():
        """Set system input, Talon mic, and output to the MacBook profile."""
        actions.app.notify(f"All audio -> {audio_device_name('summary_macbook')}")
        _set_system_input("system_input_macbook")
        actions.sound.set_microphone(audio_device_name("talon_mic_macbook"))
        _set_system_output("system_output_macbook")
