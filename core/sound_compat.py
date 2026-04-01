import subprocess
from pathlib import Path

from talon import Module, app, cron

mod = Module()

_SOUND_DIR = Path(__file__).resolve().parents[1] / "assets" / "sounds"
_SOUND_FILES = {
    "play_bell_high": _SOUND_DIR / "bike_bell_high.wav",
    "play_cancel": _SOUND_DIR / "failure.wav",
    "play_ding": _SOUND_DIR / "bike_bell_low.wav",
    "play_glass_tap": _SOUND_DIR / "glass_tap.wav",
    "play_tap": _SOUND_DIR / "tap.wav",
    "play_thunk": _SOUND_DIR / "thunk.wav",
    "play_wood_hit": _SOUND_DIR / "wood_hit.wav",
}
_ACTIVE_PROCS: set[subprocess.Popen] = set()
_PROC_POLL_JOB = None


def _poll_active_processes() -> None:
    global _ACTIVE_PROCS, _PROC_POLL_JOB
    _ACTIVE_PROCS = {proc for proc in _ACTIVE_PROCS if proc.poll() is None}
    if not _ACTIVE_PROCS and _PROC_POLL_JOB is not None:
        cron.cancel(_PROC_POLL_JOB)
        _PROC_POLL_JOB = None


def _track_process(proc: subprocess.Popen) -> None:
    global _PROC_POLL_JOB
    _ACTIVE_PROCS.add(proc)
    if _PROC_POLL_JOB is None:
        _PROC_POLL_JOB = cron.interval("200ms", _poll_active_processes)


def _play_sound(action_name: str) -> None:
    sound_path = _SOUND_FILES[action_name]
    if not sound_path.is_file():
        return

    if app.platform == "mac":
        try:
            proc = subprocess.Popen(
                ["afplay", str(sound_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            _track_process(proc)
        except Exception:
            return


@mod.action_class
class Actions:
    def play_thunk():
        """Play a thunk sound."""
        _play_sound("play_thunk")

    def play_wood_hit():
        """Play a wood hit sound."""
        _play_sound("play_wood_hit")

    def play_glass_tap():
        """Play a glass tap sound."""
        _play_sound("play_glass_tap")

    def play_ding():
        """Play a confirmation ding."""
        _play_sound("play_ding")

    def play_cancel():
        """Play a cancellation sound."""
        _play_sound("play_cancel")

    def play_tap():
        """Play a tap sound."""
        _play_sound("play_tap")

    def play_bell_high():
        """Play a high bell sound."""
        _play_sound("play_bell_high")
