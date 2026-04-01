"""Shared configuration helpers for note-related scripts."""

from pathlib import Path

from user.talon_rebecca.core import local_config

_DEFAULT_ARTICLE_LIBRARY_DIR = Path.home() / "Zotero" / "outputs" / "library_markdown_output"
_PRIVATE_NOTE_PATHS_CONFIG = local_config.settings_path("note_paths.json", private=True)
_PUBLIC_NOTE_PATHS_CONFIG = local_config.settings_path("note_paths.json", private=False)


def note_paths_config() -> dict:
    """Load the first valid note-paths config, preferring private settings."""
    return local_config.load_first_json_object(
        (_PRIVATE_NOTE_PATHS_CONFIG, _PUBLIC_NOTE_PATHS_CONFIG)
    )


def configured_path(key: str) -> Path | None:
    """Return a configured filesystem path for *key*, if present."""
    return local_config.configured_path(note_paths_config(), key)


def article_library_dir() -> Path:
    """Return the root directory containing converted article markdown files."""
    return configured_path("article_library_dir") or _DEFAULT_ARTICLE_LIBRARY_DIR
