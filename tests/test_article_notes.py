"""Tests for notes/article_notes_actions.py helper functions."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.notes.article_notes_actions as mod
    import user.talon_rebecca.notes.article_notes_domain as domain
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    class TestFindArticleFromTitle:
        """Tests for _find_article_from_title (window-title parsing)."""

        def test_normal_title(self, library_dir, window_title):
            folder = library_dir / "my_paper_abc123"
            folder.mkdir()
            article = folder / "my_paper_abc123.md"
            article.write_text("# My Paper\n")

            window_title("my_paper_abc123.md — my_paper_abc123 — Cursor")
            assert domain.find_article_from_title(
                "my_paper_abc123.md — my_paper_abc123 — Cursor", library_dir
            ) == article

        def test_modified_indicator(self, library_dir, window_title):
            """The ● prefix (unsaved changes) should be stripped."""
            folder = library_dir / "my_paper_abc123"
            folder.mkdir()
            article = folder / "my_paper_abc123.md"
            article.write_text("# My Paper\n")

            window_title("● my_paper_abc123.md — my_paper_abc123 — Cursor")
            assert domain.find_article_from_title(
                "● my_paper_abc123.md — my_paper_abc123 — Cursor", library_dir
            ) == article

        def test_notes_suffix_resolves_to_parent(self, library_dir, window_title):
            """Viewing *_notes.md* should resolve back to the parent article."""
            folder = library_dir / "my_paper_abc123"
            folder.mkdir()
            article = folder / "my_paper_abc123.md"
            article.write_text("# My Paper\n")
            (folder / "my_paper_abc123_notes.md").write_text("# Notes\n")

            window_title("my_paper_abc123_notes.md — my_paper_abc123 — Cursor")
            assert domain.find_article_from_title(
                "my_paper_abc123_notes.md — my_paper_abc123 — Cursor", library_dir
            ) == article

        def test_citation_suffix_resolves_to_parent(self, library_dir, window_title):
            """Viewing *_citation.md* should resolve back to the parent article."""
            folder = library_dir / "my_paper_abc123"
            folder.mkdir()
            article = folder / "my_paper_abc123.md"
            article.write_text("# My Paper\n")

            window_title("my_paper_abc123_citation.md — my_paper_abc123 — Cursor")
            assert domain.find_article_from_title(
                "my_paper_abc123_citation.md — my_paper_abc123 — Cursor", library_dir
            ) == article

        def test_non_md_file_returns_none(self, library_dir, window_title):
            window_title("script.py — project — Cursor")
            assert domain.find_article_from_title("script.py — project — Cursor", library_dir) is None

        def test_no_matching_file_returns_none(self, library_dir, window_title):
            window_title("nonexistent.md — folder — Cursor")
            assert domain.find_article_from_title(
                "nonexistent.md — folder — Cursor", library_dir
            ) is None

    class TestGetArticleTitle:
        def test_extracts_h1(self, tmp_path):
            md = tmp_path / "paper.md"
            md.write_text("# The Great Paper\n\nBody text.\n")
            assert domain.get_article_title(md) == "The Great Paper"

        def test_falls_back_to_filename(self, tmp_path):
            md = tmp_path / "some_paper_name.md"
            md.write_text("No heading here.\n")
            assert domain.get_article_title(md) == "some paper name"

        def test_missing_file_falls_back(self, tmp_path):
            md = tmp_path / "missing.md"
            assert domain.get_article_title(md) == "missing"

    class TestNotesPathFor:
        def test_derives_notes_path(self, tmp_path):
            article = tmp_path / "folder" / "paper.md"
            expected = tmp_path / "folder" / "paper_notes.md"
            assert domain.notes_path_for(article) == expected

    class TestEnsureNotesFile:
        def test_creates_notes_file(self, tmp_path):
            folder = tmp_path / "paper_folder"
            folder.mkdir()
            article = folder / "paper.md"
            article.write_text("# My Great Paper\n\nBody.\n")

            notes = domain.ensure_notes_file(article)
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

            notes1 = domain.ensure_notes_file(article)

            with open(notes1, "a", encoding="utf-8") as f:
                f.write("extra line\n")

            notes2 = domain.ensure_notes_file(article)
            content2 = notes2.read_text()
            assert "extra line" in content2

    class TestAddTag:
        def _make_notes(self, tmp_path, tags_line="**Tags**:"):
            notes = tmp_path / "paper_notes.md"
            notes.write_text(
                f"# Notes: Paper\n\n**Source**: [paper.md](paper.md)\n{tags_line}\n\n---\n\n"
            )
            return notes

        def test_adds_first_tag(self, tmp_path):
            notes = self._make_notes(tmp_path)
            result = domain.add_tag(notes, "important")
            assert result is True
            assert "#important" in notes.read_text()

        def test_appends_second_tag(self, tmp_path):
            notes = self._make_notes(tmp_path, tags_line="**Tags**: #read")
            result = domain.add_tag(notes, "important")
            assert result is True
            content = notes.read_text()
            assert "#read" in content
            assert "#important" in content

        def test_rejects_duplicate(self, tmp_path):
            notes = self._make_notes(tmp_path, tags_line="**Tags**: #important")
            result = domain.add_tag(notes, "important")
            assert result is False

    class TestFormattingHelpers:
        def test_normalize_excerpt_collapses_internal_whitespace(self):
            assert domain.normalize_excerpt("Line one\n  line two\tline three") == (
                "Line one line two line three"
            )

        def test_append_excerpt_writes_blockquote(self, tmp_path):
            notes = tmp_path / "paper_notes.md"
            notes.write_text("", encoding="utf-8")

            domain.append_excerpt(notes, "First line\n second line")

            assert notes.read_text(encoding="utf-8") == "> First line second line\n\n"

        def test_append_timestamped_note_writes_bullet(self, tmp_path):
            notes = tmp_path / "paper_notes.md"
            notes.write_text("", encoding="utf-8")

            domain.append_timestamped_note(notes, "capture this")

            content = notes.read_text(encoding="utf-8")
            assert content.startswith("- [")
            assert "capture this" in content

    class TestArticleActions:
        def test_article_copy_to_notes_appends_cleaned_selection(
            self, library_dir, window_title
        ):
            folder = library_dir / "my_paper_abc123"
            folder.mkdir()
            article = folder / "my_paper_abc123.md"
            article.write_text("# My Paper\n", encoding="utf-8")
            window_title("my_paper_abc123.md — my_paper_abc123 — Cursor")

            ding_calls = []
            actions.register_test_action(
                "edit", "selected_text", lambda: "First line\n second line"
            )
            actions.register_test_action("user", "play_ding", lambda: ding_calls.append(1))
            actions.register_test_action("user", "play_thunk", lambda: None)

            actions.user.article_copy_to_notes()

            notes = folder / "my_paper_abc123_notes.md"
            assert "> First line second line" in notes.read_text(encoding="utf-8")
            assert len(ding_calls) == 1

        def test_article_open_notes_notifies_when_context_is_not_article(
            self, window_title, monkeypatch
        ):
            window_title("scratch.md — misc — Cursor")

            thunk_calls = []
            open_calls = []
            actions.register_test_action(
                "user", "play_thunk", lambda: thunk_calls.append(1)
            )
            monkeypatch.setattr(
                mod,
                "open_path_in_macos_app",
                lambda app_name, path: open_calls.append((app_name, path)),
            )

            actions.user.article_open_notes()

            assert len(thunk_calls) == 1
            assert open_calls == []
            assert ("Article Notes", "Not viewing a library article") in app.notifications
