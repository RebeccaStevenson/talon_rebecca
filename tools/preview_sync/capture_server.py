#!/usr/bin/env python3
"""Entrypoint facade for the preview-sync HTTP capture service."""

from __future__ import annotations

import os
from http.server import ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace

from user.talon_rebecca.core import local_config
from user.talon_rebecca.notes import note_file_io
from user.talon_rebecca.tools.preview_sync import config as config_helpers
from user.talon_rebecca.tools.preview_sync import http_api
from user.talon_rebecca.tools.preview_sync import logging_utils
from user.talon_rebecca.tools.preview_sync.pins import PinnedSources
from user.talon_rebecca.tools.preview_sync.resolver import (
    is_allowed_origin,
    normalize_stem,
    resolve_by_hints,
    resolve_source_path,
    sanitize_scope,
    sanitize_source_hints,
)
from user.talon_rebecca.tools.preview_sync.speech import SpeechController

HOST = "127.0.0.1"
PORT = 27832
_PUBLIC_ROOTS_CONFIG = local_config.settings_path("preview_sync_roots.json", private=False)
PRIVATE_ROOTS_CONFIG = local_config.settings_path("preview_sync_roots.json", private=True)
ROOTS_CONFIG = _PUBLIC_ROOTS_CONFIG
LOG_FILE = Path(__file__).resolve().parent / "preview_sync.log"
MAX_SENTENCE_CHARS = 4000
MAX_HINTS = 8
MAX_HINT_CHARS = 240
_RESOLVED_URL_CACHE: dict[str, Path] = {}
_PIN_STORE = PinnedSources()
_SPEECH = SpeechController()


class PreviewSyncError(Exception):
    """Raised for user-facing preview-sync failures."""


def default_roots() -> list[Path]:
    """Return fallback roots when no config exists."""
    return config_helpers.default_roots()


def roots_config_candidates() -> list[Path]:
    """Return config candidates in priority order."""
    return config_helpers.roots_config_candidates(
        ROOTS_CONFIG,
        _PUBLIC_ROOTS_CONFIG,
        PRIVATE_ROOTS_CONFIG,
    )


def preferred_roots_config_path() -> Path:
    """Return the config file preview-sync should prefer editing."""
    return config_helpers.preferred_roots_config_path(
        ROOTS_CONFIG,
        _PUBLIC_ROOTS_CONFIG,
        PRIVATE_ROOTS_CONFIG,
    )


def load_roots() -> list[Path]:
    """Load valid preview-sync roots from public/private config."""
    return config_helpers.load_roots(
        ROOTS_CONFIG,
        _PUBLIC_ROOTS_CONFIG,
        PRIVATE_ROOTS_CONFIG,
    )


def _get_speak_proc():
    return _SPEECH.get_proc()


def _is_speaking() -> bool:
    return _SPEECH.is_speaking()


def _stop_speaking() -> None:
    _SPEECH.stop()


def _start_speaking_system(sentence: str) -> None:
    try:
        _SPEECH.start(sentence)
    except ValueError as exc:
        raise PreviewSyncError(str(exc)) from exc


def _normalize_stem(value: str) -> str:
    return normalize_stem(value)


def _resolve_by_hints(source_hints: list[str] | None) -> Path | None:
    return resolve_by_hints(source_hints, load_roots())


def _is_allowed_origin(origin: str | None) -> bool:
    return is_allowed_origin(origin)


def _sanitize_source_hints(raw_hints) -> list[str]:
    return sanitize_source_hints(
        raw_hints,
        max_hints=MAX_HINTS,
        max_hint_chars=MAX_HINT_CHARS,
    )


def _sanitize_scope(raw_scope: str | None, page_url: str) -> str:
    return sanitize_scope(raw_scope, page_url)


def _resolve_source(page_url: str, source_hints: list[str] | None = None) -> Path:
    roots = load_roots()
    hinted = resolve_by_hints(source_hints, roots)
    if hinted:
        return hinted

    resolved = resolve_source_path(page_url, roots, _RESOLVED_URL_CACHE)
    if resolved:
        return resolved

    raise PreviewSyncError(
        "Could not resolve source file from URL. Update your preview_sync_roots.json settings with the project root."
    )


def _set_pinned_source(scope: str, source_path: Path) -> None:
    _PIN_STORE.set(scope, source_path)


def _get_pinned_source(scope: str) -> Path | None:
    return _PIN_STORE.get(scope)


def _clear_pinned_source(scope: str | None = None) -> None:
    _PIN_STORE.clear(scope)


def _log_event(event: str, **fields) -> None:
    logging_utils.log_event(LOG_FILE, event, **fields)


def notes_path_for(source_path: Path) -> Path:
    """Return the preview-sync notes path for a source file."""
    return note_file_io.notes_path_for(source_path, in_subdir=True)


def ensure_notes_file(source_path: Path, notes_path: Path) -> Path:
    """Create the preview-sync notes file if needed."""
    relative_source = Path(os.path.relpath(source_path, start=notes_path.parent))
    return note_file_io.ensure_notes_file(
        notes_path,
        title=source_path.stem.replace("_", " "),
        source_name=source_path.name,
        source_link=relative_source.as_posix(),
    )


def append_capture(
    sentence: str,
    url: str,
    source_hints: list[str] | None = None,
    pinned_source: Path | None = None,
) -> tuple[Path, Path]:
    """Append a captured sentence to the resolved notes file."""
    if not sentence or not sentence.strip():
        raise PreviewSyncError("No sentence to capture")
    if len(sentence) > MAX_SENTENCE_CHARS:
        raise PreviewSyncError(f"Sentence too long (>{MAX_SENTENCE_CHARS} chars)")

    source_path = pinned_source if pinned_source else _resolve_source(url, source_hints)
    notes_path = notes_path_for(source_path)
    ensure_notes_file(source_path, notes_path)
    note_file_io.append_blockquote(notes_path, sentence)

    clean = note_file_io.normalize_excerpt(sentence)
    _log_event(
        "capture_ok",
        source=source_path,
        notes=notes_path,
        sentence=clean[:180],
        sentence_len=len(clean),
        url=url,
        pinned=bool(pinned_source),
    )
    return notes_path, source_path


_API = SimpleNamespace(
    append_capture=append_capture,
    clear_pinned_source=_clear_pinned_source,
    error_class=PreviewSyncError,
    get_pinned_source=_get_pinned_source,
    is_allowed_origin=_is_allowed_origin,
    is_speaking=_is_speaking,
    log_event=_log_event,
    resolve_source=_resolve_source,
    sanitize_scope=_sanitize_scope,
    sanitize_source_hints=_sanitize_source_hints,
    set_pinned_source=_set_pinned_source,
    start_speaking=_start_speaking_system,
    stop_speaking=_stop_speaking,
)

Handler = http_api.create_handler(_API)


def main() -> None:
    """Run the preview-sync HTTP server forever."""
    with ThreadingHTTPServer((HOST, PORT), Handler) as server:
        server.serve_forever(poll_interval=0.5)


if __name__ == "__main__":
    main()
