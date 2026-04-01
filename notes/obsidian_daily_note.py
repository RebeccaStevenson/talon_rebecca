"""Actions for opening and verifying Obsidian daily notes."""

from pathlib import Path

from talon import Module, actions, app
from user.talon_rebecca.notes import daily_note_domain as domain
from user.talon_rebecca.notes.note_config import configured_path

mod = Module()

_DAILY_DIR_OVERRIDE: Path | None = None
_CURSOR_OPEN_SETTLE = "2500ms"


def _set_output_shokz() -> None:
    """Set macOS system audio output to the canonical Shokz device."""
    actions.user.audio_set_system_output_shokz()


def _daily_dir() -> Path:
    if _DAILY_DIR_OVERRIDE is not None:
        return _DAILY_DIR_OVERRIDE

    vault_dir = configured_path("obsidian_vault_dir")
    if vault_dir is None:
        vault_dir = Path.home() / "notes"
    return vault_dir / "daily"


def _daily_note_path() -> Path:
    """Return the path to today's daily note."""
    return domain.daily_note_path(_daily_dir())


def _ensure_daily_note() -> Path:
    """Create today's daily note with a date header if it doesn't exist."""
    return domain.ensure_daily_note(_daily_dir())


def _append_timestamp_section(note_path: Path) -> int:
    """Append a fresh timestamp section and return the resulting last line number."""
    return domain.append_timestamp_section(note_path)


def _open_note_in_cursor(note_path: Path) -> None:
    """Open the note in Cursor and wait for the editor to settle."""
    actions.user.open_cursor_workspace(str(note_path), fallback_to_terminal=False)
    actions.sleep(_CURSOR_OPEN_SETTLE)


def _jump_to_line_end(line_number: int) -> None:
    """Jump Cursor to the requested line and move to end-of-line."""
    actions.key("ctrl-g")
    actions.sleep("300ms")
    actions.insert(str(line_number))
    actions.key("enter")
    actions.sleep("200ms")
    actions.key("end")
    actions.sleep("100ms")


def _daily_note_status(note_path: Path, now=None) -> tuple[bool, str]:
    """Return whether the daily note looks current and populated, plus a status line."""
    return domain.daily_note_status(note_path, now=now)


@mod.action_class
class Actions:
    def daily_note_start() -> None:
        """Open today's daily note in Cursor, append timestamp, play sound, start SuperWhisper normal mode."""
        note_path = _ensure_daily_note()
        line_count = _append_timestamp_section(note_path)
        _open_note_in_cursor(note_path)
        _jump_to_line_end(line_count)

        # Sync system audio output to Talon's device, then play confirmation
        _set_output_shokz()
        actions.user.play_ding()

        # Start SuperWhisper in normal mode (mirrors "whisper normal" command)
        actions.user.whisper_normal()

    def daily_note_check() -> None:
        """Save the focused daily note editor and verify recent content exists."""
        note_path = _daily_note_path()

        if not note_path.exists():
            actions.user.play_cancel()
            app.notify("Daily Note Check", "No daily note found for today.")
            return

        # Save the currently focused editor window before reading the file.
        actions.key("cmd-s")
        actions.sleep("500ms")
        is_ok, status = _daily_note_status(note_path)

        _set_output_shokz()
        if is_ok:
            actions.user.play_ding()
            app.notify("Daily Note: OK", status)
        else:
            actions.user.play_cancel()
            app.notify("Daily Note: Check", status)
