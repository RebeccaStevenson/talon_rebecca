"""Tests for notes/article_notes_actions.py helper functions."""

from pathlib import Path

import pytest

from notes.article_notes_actions import (
    _add_tag,
    _ensure_notes_file,
    _find_article_from_title,
    _get_article_title,
    _notes_path_for,
)


# ---------------------------------------------------------------------------
# _find_article_from_title
# ---------------------------------------------------------------------------


class TestFindArticleFromTitle:
    """Tests for _find_article_from_title (window-title parsing)."""

    def test_normal_title(self, library_dir, window_title):
        folder = library_dir / "my_paper_abc123"
        folder.mkdir()
        article = folder / "my_paper_abc123.md"
        article.write_text("# My Paper\n")

        window_title("my_paper_abc123.md — my_paper_abc123 — Cursor")
        assert _find_article_from_title() == article

    def test_modified_indicator(self, library_dir, window_title):
        """The ● prefix (unsaved changes) should be stripped."""
        folder = library_dir / "my_paper_abc123"
        folder.mkdir()
        article = folder / "my_paper_abc123.md"
        article.write_text("# My Paper\n")

        window_title("● my_paper_abc123.md — my_paper_abc123 — Cursor")
        assert _find_article_from_title() == article

    def test_notes_suffix_resolves_to_parent(self, library_dir, window_title):
        """Viewing *_notes.md* should resolve back to the parent article."""
        folder = library_dir / "my_paper_abc123"
        folder.mkdir()
        article = folder / "my_paper_abc123.md"
        article.write_text("# My Paper\n")
        # The notes file also exists
        (folder / "my_paper_abc123_notes.md").write_text("# Notes\n")

        window_title("my_paper_abc123_notes.md — my_paper_abc123 — Cursor")
        assert _find_article_from_title() == article

    def test_citation_suffix_resolves_to_parent(self, library_dir, window_title):
        """Viewing *_citation.md* should resolve back to the parent article."""
        folder = library_dir / "my_paper_abc123"
        folder.mkdir()
        article = folder / "my_paper_abc123.md"
        article.write_text("# My Paper\n")

        window_title("my_paper_abc123_citation.md — my_paper_abc123 — Cursor")
        assert _find_article_from_title() == article

    def test_non_md_file_returns_none(self, library_dir, window_title):
        window_title("script.py — project — Cursor")
        assert _find_article_from_title() is None

    def test_no_matching_file_returns_none(self, library_dir, window_title):
        window_title("nonexistent.md — folder — Cursor")
        assert _find_article_from_title() is None


# ---------------------------------------------------------------------------
# _get_article_title
# ---------------------------------------------------------------------------


class TestGetArticleTitle:
    def test_extracts_h1(self, tmp_path):
        md = tmp_path / "paper.md"
        md.write_text("# The Great Paper\n\nBody text.\n")
        assert _get_article_title(md) == "The Great Paper"

    def test_falls_back_to_filename(self, tmp_path):
        md = tmp_path / "some_paper_name.md"
        md.write_text("No heading here.\n")
        assert _get_article_title(md) == "some paper name"

    def test_missing_file_falls_back(self, tmp_path):
        md = tmp_path / "missing.md"
        assert _get_article_title(md) == "missing"


# ---------------------------------------------------------------------------
# _notes_path_for
# ---------------------------------------------------------------------------


class TestNotesPathFor:
    def test_derives_notes_path(self, tmp_path):
        article = tmp_path / "folder" / "paper.md"
        expected = tmp_path / "folder" / "paper_notes.md"
        assert _notes_path_for(article) == expected


# ---------------------------------------------------------------------------
# _ensure_notes_file
# ---------------------------------------------------------------------------


class TestEnsureNotesFile:
    def test_creates_notes_file(self, tmp_path):
        folder = tmp_path / "paper_folder"
        folder.mkdir()
        article = folder / "paper.md"
        article.write_text("# My Great Paper\n\nBody.\n")

        notes = _ensure_notes_file(article)
        assert notes.exists()
        content = notes.read_text()
        assert "# Notes: My Great Paper" in content
        assert "**Source**:" in content
        assert "**Tags**:" in content

    def test_idempotent(self, tmp_path):
        folder = tmp_path / "paper_folder"
        folder.mkdir()
        article = folder / "paper.md"
        article.write_text("# Paper\n")

        notes1 = _ensure_notes_file(article)
        content1 = notes1.read_text()

        # Append something
        with open(notes1, "a") as f:
            f.write("extra line\n")

        notes2 = _ensure_notes_file(article)
        content2 = notes2.read_text()

        # Should NOT have overwritten — the extra line should still be there
        assert "extra line" in content2


# ---------------------------------------------------------------------------
# _add_tag
# ---------------------------------------------------------------------------


class TestAddTag:
    def _make_notes(self, tmp_path, tags_line="**Tags**:"):
        notes = tmp_path / "paper_notes.md"
        notes.write_text(
            f"# Notes: Paper\n\n**Source**: [paper.md](paper.md)\n{tags_line}\n\n---\n\n"
        )
        return notes

    def test_adds_first_tag(self, tmp_path):
        notes = self._make_notes(tmp_path)
        result = _add_tag(notes, "important")
        assert result is True
        assert "#important" in notes.read_text()

    def test_appends_second_tag(self, tmp_path):
        notes = self._make_notes(tmp_path, tags_line="**Tags**: #read")
        result = _add_tag(notes, "important")
        assert result is True
        content = notes.read_text()
        assert "#read" in content
        assert "#important" in content

    def test_rejects_duplicate(self, tmp_path):
        notes = self._make_notes(tmp_path, tags_line="**Tags**: #important")
        result = _add_tag(notes, "important")
        assert result is False
