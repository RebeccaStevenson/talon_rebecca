"""Pure helpers for Obsidian daily note workflows."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def daily_note_path(daily_dir: Path, now: datetime | None = None) -> Path:
    """Return today's daily note path inside *daily_dir*."""
    current = now or datetime.now()
    return daily_dir / f"{current.strftime('%Y-%m-%d')}.md"


def ensure_daily_note(daily_dir: Path, now: datetime | None = None) -> Path:
    """Create today's daily note with a date header if needed."""
    path = daily_note_path(daily_dir, now=now)
    daily_dir.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        current = now or datetime.now()
        path.write_text(f"# {current.strftime('%Y-%m-%d')}\n\n", encoding="utf-8")
    return path


def append_timestamp_section(note_path: Path, now: datetime | None = None) -> int:
    """Append a new timestamp section and return the line number to jump to."""
    current = now or datetime.now()
    timestamp = current.strftime("%-I:%M %p")
    with open(note_path, "a", encoding="utf-8") as file:
        file.write(f"## {timestamp}\n\n")
    return note_path.read_text(encoding="utf-8").count("\n") + 1


def daily_note_status(
    note_path: Path, now: datetime | None = None
) -> tuple[bool, str]:
    """Return whether the daily note looks current plus a status line."""
    current = now or datetime.now()
    mod_time = datetime.fromtimestamp(note_path.stat().st_mtime)
    minutes_ago = (current - mod_time).total_seconds() / 60

    lines = note_path.read_text(encoding="utf-8").strip().split("\n")
    last_ts_idx = -1
    for index, line in enumerate(lines):
        if line.startswith("## ") and ("AM" in line or "PM" in line):
            last_ts_idx = index

    has_content = False
    if last_ts_idx >= 0:
        remaining = "\n".join(lines[last_ts_idx + 1 :]).strip()
        has_content = bool(remaining)

    if minutes_ago <= 5:
        time_status = f"Saved {minutes_ago:.0f}m ago"
    else:
        time_status = f"Last modified {minutes_ago:.0f}m ago"

    content_status = "Content added" if has_content else "No new content after timestamp"
    return has_content and minutes_ago <= 5, f"{time_status} | {content_status}"
