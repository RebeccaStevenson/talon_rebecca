"""Tests for note configuration helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.notes.note_config as note_config

    def test_article_library_dir_uses_configured_path(monkeypatch, tmp_path):
        configured = tmp_path / "library"
        seen_keys = []

        def _configured_path(key):
            seen_keys.append(key)
            return configured

        monkeypatch.setattr(note_config, "configured_path", _configured_path)

        assert note_config.article_library_dir() == configured
        assert seen_keys == ["article_library_dir"]

    def test_article_library_dir_falls_back_when_unconfigured(monkeypatch):
        monkeypatch.setattr(note_config, "configured_path", lambda key: None)

        assert note_config.article_library_dir().name == "library_markdown_output"
