"""Shared pytest fixtures for talon_rebecca tests."""

import sys

if "pytest" in sys.modules:
    import textwrap

    import pytest
    from talon import ui

    @pytest.fixture()
    def tmp_article(tmp_path):
        """Create a temp directory with a sample article .md file.

        Yields the path to the article markdown file. The directory
        structure mirrors the real library layout::

            tmp_path/
              Some_Article_abc123/
                Some_Article_abc123.md
        """
        folder = tmp_path / "Some_Article_abc123"
        folder.mkdir()
        article = folder / "Some_Article_abc123.md"
        article.write_text(
            textwrap.dedent("""\
                # A Sample Article Title

                This is the body of the article.
            """),
            encoding="utf-8",
        )
        return article

    @pytest.fixture()
    def library_dir(tmp_path, monkeypatch):
        """Monkeypatch the article library root to point at *tmp_path*."""
        import user.talon_rebecca.notes.note_config as note_config

        monkeypatch.setattr(note_config, "article_library_dir", lambda: tmp_path)
        return tmp_path

    @pytest.fixture()
    def window_title():
        """Helper to set the stub ui active-window title."""

        def _set(title: str):
            ui._window.title = title

        return _set

    @pytest.fixture()
    def talon_platform(monkeypatch):
        """Temporarily set the Talon platform stub."""

        def _set(value: str):
            monkeypatch.setattr("talon.app.platform", value)

        return _set
