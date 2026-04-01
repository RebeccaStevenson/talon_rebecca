"""Pure helpers for journal article note files."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from user.talon_rebecca.notes import note_file_io


def find_article_from_title(title: str, library_dir: Path) -> Optional[Path]:
    """Resolve a library article path from an editor window title."""
    parts = re.split(r"\s[—–-]\s", title)
    if not parts:
        return None

    filename = parts[0].strip().lstrip("●◦ ").strip()
    if not filename.endswith(".md"):
        return None

    stem = Path(filename).stem
    for suffix in ("_notes", "_citation"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            filename = f"{stem}.md"
            break

    direct = library_dir / stem / filename
    if direct.exists():
        return direct

    matches = list(library_dir.rglob(filename))
    return matches[0] if matches else None


def get_article_title(article_path: Path) -> str:
    """Extract the first H1 heading from an article markdown file."""
    try:
        with open(article_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return article_path.stem.replace("_", " ")


def notes_path_for(article_path: Path) -> Path:
    """Return the companion notes file path for an article markdown file."""
    return note_file_io.notes_path_for(article_path)


def ensure_notes_file(article_path: Path) -> Path:
    """Create the notes file with a standard header if it does not exist."""
    notes_path = notes_path_for(article_path)
    return note_file_io.ensure_notes_file(
        notes_path,
        title=get_article_title(article_path),
        source_name=article_path.name,
        source_link=article_path.name,
    )


def add_tag(notes_path: Path, tag: str) -> bool:
    """Add a hashtag to the Tags line, returning False if already present."""
    content = notes_path.read_text(encoding="utf-8")
    marker = f"#{tag}"
    lines = content.split("\n")
    for index, line in enumerate(lines):
        if line.startswith("**Tags**"):
            if marker in line:
                return False
            if line.rstrip() in ("**Tags**:", "**Tags**"):
                lines[index] = f"**Tags**: {marker}"
            else:
                lines[index] = f"{line} {marker}"
            notes_path.write_text("\n".join(lines), encoding="utf-8")
            return True
    return False


def normalize_excerpt(text: str) -> str:
    """Collapse internal whitespace so excerpts stay single-line."""
    return note_file_io.normalize_excerpt(text)


def append_excerpt(notes_path: Path, text: str) -> None:
    """Append a markdown blockquote excerpt to a notes file."""
    note_file_io.append_blockquote(notes_path, text)


def append_timestamped_note(
    notes_path: Path, text: str, now: datetime | None = None
) -> None:
    """Append a timestamped bullet note to a notes file."""
    timestamp = (now or datetime.now()).strftime("%Y-%m-%d %H:%M")
    with open(notes_path, "a", encoding="utf-8") as file:
        file.write(f"- [{timestamp}] {text.strip()}\n\n")
