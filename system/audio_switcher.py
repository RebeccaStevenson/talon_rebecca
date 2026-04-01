"""Shared helpers for switching macOS system audio devices."""

from __future__ import annotations

from dataclasses import dataclass
import subprocess
from pathlib import Path
from typing import Literal

from talon import actions

AudioDeviceType = Literal["input", "output"]
_SWITCH_AUDIO_SOURCE_CANDIDATES = (
    "/opt/homebrew/bin/SwitchAudioSource",
    "/usr/local/bin/SwitchAudioSource",
)


class AudioSwitcherError(RuntimeError):
    """Raised when SwitchAudioSource is unavailable or returns an error."""


def switch_audio_source_path() -> str | None:
    """Return the installed SwitchAudioSource executable path."""
    for candidate in _SWITCH_AUDIO_SOURCE_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def best_device_match(devices: list[str], desired: str) -> str | None:
    """Return the best device match by exact, case-insensitive, then substring match."""
    desired_stripped = desired.strip()
    if not desired_stripped:
        return None

    for device in devices:
        if device == desired_stripped:
            return device

    desired_lower = desired_stripped.lower()
    for device in devices:
        if device.lower() == desired_lower:
            return device

    for device in devices:
        if desired_lower in device.lower():
            return device

    return None


def _switch_audio_source(device_type: AudioDeviceType, *args: str) -> subprocess.CompletedProcess[str]:
    exe = switch_audio_source_path()
    if not exe:
        raise AudioSwitcherError(
            "SwitchAudioSource not found. Install with: brew install switchaudio-osx"
        )

    result = subprocess.run(
        [exe, *args, "-t", device_type],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise AudioSwitcherError(f"SwitchAudioSource failed: {stderr}")

    return result


def get_current_device(device_type: AudioDeviceType) -> str | None:
    """Return the current device name for the requested input/output type."""
    result = _switch_audio_source(device_type, "-c")
    device = (result.stdout.splitlines()[:1] or [""])[0].strip()
    return device or None


def list_devices(device_type: AudioDeviceType) -> list[str]:
    """Return the available device names for the requested input/output type."""
    result = _switch_audio_source(device_type, "-a")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def set_device(device_type: AudioDeviceType, device: str) -> None:
    """Set the requested input/output device by exact name."""
    exe = switch_audio_source_path()
    if not exe:
        raise AudioSwitcherError(
            "SwitchAudioSource not found. Install with: brew install switchaudio-osx"
        )

    try:
        subprocess.run(
            [exe, "-t", device_type, "-s", device],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        stderr = (error.stderr or "").strip()
        raise AudioSwitcherError(f"Failed to set system {device_type}: {stderr or device}") from error


@dataclass
class AudioDeviceController:
    """Shared orchestration for an audio device picker flow."""

    device_type: AudioDeviceType
    device_label: str
    saved_device_path: Path | None = None

    def _notify_error(self, error: AudioSwitcherError) -> None:
        actions.app.notify(str(error))

    def current_device(self) -> str | None:
        """Return the current device name, or notify and return None on failure."""
        try:
            return get_current_device(self.device_type)
        except AudioSwitcherError as error:
            self._notify_error(error)
            return None

    def list_devices(self) -> list[str]:
        """Return the available devices, or notify and return an empty list on failure."""
        try:
            return list_devices(self.device_type)
        except AudioSwitcherError as error:
            self._notify_error(error)
            return []

    def set_device(self, device: str) -> bool:
        """Set the current device and notify on success."""
        try:
            set_device(self.device_type, device)
        except AudioSwitcherError as error:
            self._notify_error(error)
            return False

        actions.app.notify(f"System {self.device_label} -> {device}")
        return True

    def preferred_device(self, desired: str) -> None:
        """Set the current device by fuzzy match."""
        devices = self.list_devices()
        if not devices:
            return

        match = best_device_match(devices, desired)
        if not match:
            actions.app.notify(f"No matching {self.device_label} device for: {desired}")
            return

        self.set_device(match)

    def save_current_device(self) -> None:
        """Persist the current device for later restoration."""
        if self.saved_device_path is None:
            raise AudioSwitcherError(f"Saving {self.device_label} devices is not supported")

        current = self.current_device()
        if not current:
            actions.app.notify(f"No current {self.device_label} device detected")
            return

        try:
            self.saved_device_path.write_text(current + "\n", encoding="utf-8")
        except OSError as error:
            actions.app.notify(f"Failed to save {self.device_label} device: {error}")
            return

        actions.app.notify(f"Saved {self.device_label} device: {current}")

    def restore_saved_device(self) -> None:
        """Restore the previously saved device."""
        if self.saved_device_path is None:
            raise AudioSwitcherError(f"Restoring {self.device_label} devices is not supported")

        try:
            saved = self.saved_device_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            actions.app.notify(f"No saved {self.device_label} device (switch first)")
            return
        except OSError as error:
            actions.app.notify(f"Failed to read saved {self.device_label} device: {error}")
            return

        if not saved:
            actions.app.notify(f"Saved {self.device_label} device was empty")
            return

        self.set_device(saved)


def toggle_picker(gui_handle, device_list: list[str], controller: AudioDeviceController) -> None:
    """Toggle an imgui picker, populating the device list when shown."""
    if gui_handle.showing:
        gui_handle.hide()
        return

    device_list[:] = controller.list_devices()
    if not device_list:
        return

    gui_handle.show()


def select_from_picker(
    index: int,
    device_list: list[str],
    controller: AudioDeviceController,
    gui_handle,
) -> None:
    """Select an item from an imgui picker and hide the picker."""
    if 1 <= index <= len(device_list):
        controller.set_device(device_list[index - 1])
        gui_handle.hide()
