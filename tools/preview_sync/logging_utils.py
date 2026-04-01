"""Logging helpers for preview sync."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def log_event(log_file: Path, event: str, **fields) -> None:
    """Append a best-effort structured log line."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    parts = [f"{key}={str(value).replace(chr(10), ' ')[:1200]}" for key, value in fields.items()]
    line = f"{timestamp} {event}"
    if parts:
        line += " " + " ".join(parts)
    line += "\n"

    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as handle:
            handle.write(line)
    except Exception:
        pass
