"""Regression tests for Talon's words_to_replace CSV handling."""

import importlib.util
from pathlib import Path


def _load_user_settings_module():
    module_path = (
        Path(__file__).resolve().parents[2] / "community" / "core" / "user_settings.py"
    )
    spec = importlib.util.spec_from_file_location(
        "community.core.user_settings", module_path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_write_csv_defaults_does_not_overwrite_existing_file(tmp_path):
    user_settings = _load_user_settings_module()
    path = tmp_path / "words_to_replace.csv"
    original = "Replacement,Original\nclaude,clod\n"
    path.write_text(original, encoding="utf-8")

    user_settings.write_csv_defaults(
        path,
        headers=("Replacement", "Original"),
        default={"cloud": "clod"},
    )

    assert path.read_text(encoding="utf-8") == original


def test_write_csv_defaults_does_not_overwrite_existing_symlink_target(tmp_path):
    user_settings = _load_user_settings_module()
    target = tmp_path / "talon_rebecca_words_to_replace.csv"
    target.write_text("Replacement,Original\nclaude,clod\n", encoding="utf-8")
    link = tmp_path / "community_words_to_replace.csv"
    link.symlink_to(target)

    user_settings.write_csv_defaults(
        link,
        headers=("Replacement", "Original"),
        default={"cloud": "clod"},
    )

    assert link.is_symlink()
    assert target.read_text(encoding="utf-8") == "Replacement,Original\nclaude,clod\n"


def test_read_csv_list_maps_original_to_replacement(tmp_path):
    user_settings = _load_user_settings_module()
    path = tmp_path / "words_to_replace.csv"
    path.write_text(
        "Replacement,Original\nclaude,clod\nclaude,cloud\n",
        encoding="utf-8",
    )

    with path.open(encoding="utf-8") as handle:
        mapping = user_settings.read_csv_list(
            handle,
            headers=("Replacement", "Original"),
        )

    assert mapping["clod"] == "claude"
    assert mapping["cloud"] == "claude"
