import os
import shlex
import signal
import tempfile
from pathlib import Path

from talon import Module, actions, clip

VOICE_SCRIPT_DIR = Path.home() / ".claude" / "hooks" / "voice_notifications"
UV_PATH = Path.home() / ".local" / "bin" / "uv"
PLAYBACK_PID_FILE = VOICE_SCRIPT_DIR / ".playback_pid"

mod = Module()


def _command_with_directory(command: str, path: Path | None) -> str:
    if not path:
        return command

    expanded = os.path.abspath(os.path.expanduser(str(path)))
    if os.name == "posix":
        return f"cd {shlex.quote(expanded)}\n{command}"

    drive, _ = os.path.splitdrive(expanded)
    safe_path = expanded.replace('"', '""')
    parts = []
    if drive:
        parts.append(drive)
    parts.append(f'cd "{safe_path}"')
    parts.append(command)
    return "\n".join(parts)


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

    shell_command = _command_with_directory(
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

    shell_command = _command_with_directory(command, VOICE_SCRIPT_DIR)

    actions.user.run_command_in_new_terminal(
        shell_command,
        close_after=False,
        post_command_delay="750ms",
    )
    actions.app.notify(notify_message)


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
