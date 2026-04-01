"""Pinned-source state for preview sync."""

from __future__ import annotations

import threading
from pathlib import Path


class PinnedSources:
    """Thread-safe in-memory map of preview scopes to source files."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sources: dict[str, Path] = {}

    def set(self, scope: str, source_path: Path) -> None:
        if not scope:
            return
        with self._lock:
            self._sources[scope] = source_path

    def get(self, scope: str) -> Path | None:
        if not scope:
            return None
        with self._lock:
            pinned = self._sources.get(scope)
        if pinned and pinned.exists():
            return pinned
        return None

    def clear(self, scope: str | None = None) -> None:
        with self._lock:
            if scope:
                self._sources.pop(scope, None)
                return
            self._sources.clear()
