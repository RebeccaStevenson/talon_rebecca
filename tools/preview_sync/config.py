"""Configuration helpers for preview-sync source resolution."""

from __future__ import annotations

from pathlib import Path

from user.talon_rebecca.core import local_config


def default_roots() -> list[Path]:
    """Return fallback roots when no config exists."""
    return [Path.home() / "localFiles"]


def roots_config_candidates(
    current_config: Path, public_config: Path, private_config: Path
) -> list[Path]:
    """Return config candidates in priority order."""
    if current_config != public_config:
        return [current_config]
    return [private_config, public_config]


def preferred_roots_config_path(
    current_config: Path, public_config: Path, private_config: Path
) -> Path:
    """Return the file that should be created or edited by default."""
    for candidate in roots_config_candidates(current_config, public_config, private_config):
        if candidate.exists():
            return candidate
    return private_config


def load_roots(
    current_config: Path,
    public_config: Path,
    private_config: Path,
) -> list[Path]:
    """Load valid preview-sync roots, creating a default config if needed."""
    config_path = preferred_roots_config_path(current_config, public_config, private_config)
    local_config.ensure_json_file(
        config_path,
        {"roots": [str(path) for path in default_roots()]},
    )

    config = local_config.load_first_json_object(
        roots_config_candidates(current_config, public_config, private_config)
    )
    if not config:
        return default_roots()

    roots = []
    for value in config.get("roots", []):
        path = Path(value).expanduser()
        if path.exists() and path.is_dir():
            roots.append(path)

    return roots or default_roots()
