"""Shared pytest fixtures for talon_rebecca tests."""

import textwrap
from pathlib import Path

import pytest

from talon import ui


@pytest.fixture()
def tmp_article(tmp_path):
    """Create a temp directory with a sample article .md file.

    Yields the path to the article markdown file.  The directory
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
    """Monkeypatch LIBRARY_DIR to point at *tmp_path*.

    Returns the tmp_path so tests can create arbitrary folder layouts.
    Must be imported *after* the module under test is loaded (pytest
    handles this automatically via the function-scoped monkeypatch).
    """
    import notes.article_notes_actions as mod

    monkeypatch.setattr(mod, "LIBRARY_DIR", tmp_path)
    return tmp_path


@pytest.fixture()
def window_title():
    """Helper to set the stub ui active-window title."""

    def _set(title: str):
        ui._window.title = title

    return _set
