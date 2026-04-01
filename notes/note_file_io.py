"""Shared note-file path, header, and excerpt helpers."""

from __future__ import annotations

from pathlib import Path

NOTE_SOURCE_SUFFIXES = ("_notes", "_citation")


def normalized_source_stem(
    source_path: Path, suffixes: tuple[str, ...] = NOTE_SOURCE_SUFFIXES
) -> str:
    """Return the source stem with note/citation suffixes stripped."""
    stem = source_path.stem
    for suffix in suffixes:
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def notes_path_for(source_path: Path, *, in_subdir: bool = False) -> Path:
    """Return the canonical notes path for a source file."""
    stem = normalized_source_stem(source_path)
    if in_subdir:
        notes_dir = source_path.parent / f"{stem}_notes"
        return notes_dir / f"{stem}_notes.md"
    return source_path.parent / f"{stem}_notes.md"


def make_notes_header(title: str, source_name: str, source_link: str) -> str:
    """Build the standard markdown header for a notes file."""
    return (
        f"# Notes: {title}\n"
        "\n"
        f"**Source**: [{source_name}]({source_link})\n"
        "**Tags**:\n"
        "\n"
        "---\n"
        "\n"
    )


def ensure_notes_file(
    notes_path: Path, *, title: str, source_name: str, source_link: str
) -> Path:
    """Create a notes file with the shared header if it does not exist."""
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    if not notes_path.exists():
        notes_path.write_text(
            make_notes_header(title, source_name, source_link),
            encoding="utf-8",
        )
    return notes_path


def normalize_excerpt(text: str) -> str:
    """Collapse internal whitespace so excerpts stay single-line."""
    return " ".join(text.strip().split())


def append_blockquote(notes_path: Path, text: str) -> None:
    """Append a markdown blockquote excerpt to a notes file."""
    clean = normalize_excerpt(text)
    with open(notes_path, "a", encoding="utf-8") as file:
        file.write(f"> {clean}\n\n")
