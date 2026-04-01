"""Shared helpers for loading local/private JSON settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SETTINGS_DIR = REPO_ROOT.parent / "talon_rebecca_private" / "settings"
PUBLIC_SETTINGS_DIR = REPO_ROOT / "settings"


def settings_path(filename: str, *, private: bool) -> Path:
    """Return the canonical private or public settings path for *filename*."""
    base_dir = PRIVATE_SETTINGS_DIR if private else PUBLIC_SETTINGS_DIR
    return base_dir / filename


def config_candidates(*paths: Path | None) -> list[Path]:
    """Return unique config candidates in the provided priority order."""
    seen: set[Path] = set()
    candidates: list[Path] = []
    for path in paths:
        if path is None:
            continue
        if path in seen:
            continue
        seen.add(path)
        candidates.append(path)
    return candidates


def load_first_json_object(paths: Iterable[Path]) -> dict:
    """Load the first valid JSON object from *paths*."""
    for path in paths:
        if not path.exists():
            continue
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(config, dict):
            return config
    return {}


def ensure_json_file(path: Path, payload: dict) -> Path:
    """Create *path* with *payload* if it does not already exist."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def configured_path(config: dict, key: str) -> Path | None:
    """Return a configured filesystem path for *key*, if present."""
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        return None
    return Path(value).expanduser()
