import os
import shlex
import signal
import subprocess
import tempfile
from pathlib import Path

from talon import Module, actions, clip, cron
from user.talon_rebecca.core import local_config
from user.talon_rebecca.core.platform_utils import command_with_directory

_PRIVATE_VOICE_NOTIFICATIONS_CONFIG = local_config.settings_path(
    "voice_notifications.json",
    private=True,
)
_PUBLIC_VOICE_NOTIFICATIONS_CONFIG = local_config.settings_path(
    "voice_notifications.json",
    private=False,
)
_DEFAULT_VOICE_SCRIPT_DIR = Path.home() / ".claude" / "hooks" / "voice_notifications"
_DEFAULT_UV_PATH = Path.home() / ".local" / "bin" / "uv"
_PLAYBACK_PROC: subprocess.Popen | None = None
_PLAYBACK_POLL_JOB = None

mod = Module()


def _voice_notifications_config() -> dict:
    return local_config.load_first_json_object(
        (_PRIVATE_VOICE_NOTIFICATIONS_CONFIG, _PUBLIC_VOICE_NOTIFICATIONS_CONFIG)
    )


def _configured_int(config: dict, key: str) -> int | None:
    value = config.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


_VOICE_CONFIG = _voice_notifications_config()
VOICE_SCRIPT_DIR = (
    local_config.configured_path(_VOICE_CONFIG, "voice_script_dir")
    or _DEFAULT_VOICE_SCRIPT_DIR
)
UV_PATH = local_config.configured_path(_VOICE_CONFIG, "uv_path") or _DEFAULT_UV_PATH
PLAYBACK_PID_FILE = (
    local_config.configured_path(_VOICE_CONFIG, "playback_pid_file")
    or VOICE_SCRIPT_DIR / ".playback_pid"
)
DEFAULT_SYSTEM_VOICE = _VOICE_CONFIG.get("default_system_voice")
if not isinstance(DEFAULT_SYSTEM_VOICE, str) or not DEFAULT_SYSTEM_VOICE.strip():
    DEFAULT_SYSTEM_VOICE = None
DEFAULT_SYSTEM_RATE = _configured_int(_VOICE_CONFIG, "default_system_rate")


def _poll_playback_process() -> None:
    global _PLAYBACK_PROC, _PLAYBACK_POLL_JOB
    if _PLAYBACK_PROC is not None and _PLAYBACK_PROC.poll() is None:
        return

    _PLAYBACK_PROC = None
    if _PLAYBACK_POLL_JOB is not None:
        cron.cancel(_PLAYBACK_POLL_JOB)
        _PLAYBACK_POLL_JOB = None


def _validate_script(script_name: str) -> bool:
    script_path = VOICE_SCRIPT_DIR / script_name

    if not script_path.exists():
        actions.app.notify(f"{script_name} not found")
        return False

    if not UV_PATH.exists():
        actions.app.notify("uv executable not found at ~/.local/bin/uv")
        return False

    return True


def _run_voice_script(script_name: str, notify_message: str):
    if not _validate_script(script_name):
        return

    shell_command = command_with_directory(
        f"{shlex.quote(str(UV_PATH))} run {script_name}",
        VOICE_SCRIPT_DIR,
    )

    actions.user.run_command_in_new_terminal(
        shell_command,
        close_after=False,
        post_command_delay="750ms",
    )
    actions.app.notify(notify_message)


def _pipe_text_to_script(script_name: str, text: str, notify_message: str):
    if not _validate_script(script_name):
        return

    try:
        tmp_file = tempfile.NamedTemporaryFile(
            "w", delete=False, encoding="utf-8", suffix=".txt"
        )
        with tmp_file:
            tmp_file.write(text)
        temp_path = Path(tmp_file.name)
    except Exception as exc:
        actions.app.notify(f"Unable to create temporary file: {exc}")
        return

    quoted_temp = shlex.quote(str(temp_path))
    command = (
        f"cat {quoted_temp} | {shlex.quote(str(UV_PATH))} run {script_name}; "
        f"rm -f {quoted_temp}"
    )

    shell_command = command_with_directory(command, VOICE_SCRIPT_DIR)

    actions.user.run_command_in_new_terminal(
        shell_command,
        close_after=False,
        post_command_delay="750ms",
    )
    actions.app.notify(notify_message)


def _speak_with_macos_say(
    text: str,
    voice: str | None = DEFAULT_SYSTEM_VOICE,
    rate: int | None = DEFAULT_SYSTEM_RATE,
):
    global _PLAYBACK_PROC, _PLAYBACK_POLL_JOB
    if not text or not text.strip():
        actions.app.notify("No text to read")
        return

    try:
        cmd = ["say"]
        # If no explicit voice/rate is provided, macOS uses the user's selected defaults.
        if voice:
            cmd.extend(["-v", voice])
        if rate:
            cmd.extend(["-r", str(rate)])
        cmd.append(text)

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as exc:
        actions.app.notify(f"say failed: {exc}")
        return
    _PLAYBACK_PROC = proc
    if _PLAYBACK_POLL_JOB is None:
        _PLAYBACK_POLL_JOB = cron.interval("200ms", _poll_playback_process)

    try:
        PLAYBACK_PID_FILE.write_text(str(proc.pid), encoding="utf-8")
    except Exception:
        pass

    actions.app.notify("Reading text with macOS say")


@mod.action_class
class VoiceNotificationActions:
    def read_claude_last_response():
        """Read the most recent Claude response aloud via the voice handler script."""
        _run_voice_script("read_last_response.py", "Reading Claude response in new terminal")

    def read_codex_last_response():
        """Read the most recent Codex response aloud via the voice handler script."""
        _run_voice_script("read_last_codex_response.py", "Reading Codex response in new terminal")

    def stop_claude_voice_playback():
        """Stop the active voice playback if running."""
        global _PLAYBACK_PROC, _PLAYBACK_POLL_JOB
        if not PLAYBACK_PID_FILE.exists():
            actions.app.notify("No voice playback is currently running")
            return

        try:
            pid_value = PLAYBACK_PID_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            actions.app.notify("Unable to read playback PID")
            return

        if not pid_value.isdigit():
            actions.app.notify("Playback PID is invalid; clearing marker")
            PLAYBACK_PID_FILE.unlink(missing_ok=True)
            return

        pid = int(pid_value)
        killed = False
        message = "Stopped voice playback"

        try:
            os.killpg(pid, signal.SIGTERM)
            killed = True
        except ProcessLookupError:
            message = "Playback process already ended"
        except PermissionError:
            message = "Permission denied stopping playback"
        except OSError:
            try:
                os.kill(pid, signal.SIGTERM)
                killed = True
            except ProcessLookupError:
                message = "Playback process already ended"
            except PermissionError:
                message = "Permission denied stopping playback"

        actions.app.notify(message if not killed else "Stopped voice playback")
        PLAYBACK_PID_FILE.unlink(missing_ok=True)
        _PLAYBACK_PROC = None
        if _PLAYBACK_POLL_JOB is not None:
            cron.cancel(_PLAYBACK_POLL_JOB)
            _PLAYBACK_POLL_JOB = None

    def stop_read_aloud():
        """Stop active read-aloud playback from any voice-notification reader."""
        actions.user.stop_claude_voice_playback()

    def read_text_aloud(text: str):
        """Read arbitrary text aloud using the voice handler."""
        if not text or not text.strip():
            actions.app.notify("No text to read")
            return
        _pipe_text_to_script("read_text.py", text, "Reading text in new terminal")

    def read_clipboard_text_aloud():
        """Read text currently on the clipboard aloud."""
        text = clip.get()
        if not text:
            actions.app.notify("Clipboard is empty")
            return
        _pipe_text_to_script("read_text.py", text, "Reading clipboard text in new terminal")

    def read_text_aloud_system(text: str):
        """Read arbitrary text aloud using macOS say for faster startup."""
        _speak_with_macos_say(text)

    def read_clipboard_text_aloud_system():
        """Read clipboard text aloud using macOS say for faster startup."""
        text = clip.get()
        if not text:
            actions.app.notify("Clipboard is empty")
            return
        _speak_with_macos_say(text)
