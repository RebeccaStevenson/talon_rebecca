"""Actions for managing journal article notes from Zotero library markdown files.

Provides voice-driven workflows for copying excerpts, tagging, and
appending dictated notes to per-article notes files that live alongside
the converted markdown in outputs/library_markdown_output/.
"""

from pathlib import Path

from talon import Context, Module, actions, app, ui
from user.talon_rebecca.core.platform_utils import open_path_in_macos_app
from user.talon_rebecca.notes import article_notes_domain as domain
from user.talon_rebecca.notes import note_config

mod = Module()

mod.list("article_tag", desc="Tags for journal article notes")

ctx = Context()
ctx.lists["user.article_tag"] = {
    "important": "important",
    "read": "read",
    "not important": "not_important",
    "to read": "to_read",
    "review": "review",
    "key paper": "key_paper",
    "methods": "methods",
    "results": "results",
}


def _find_article_from_title() -> Path | None:
    """Find the article markdown from the active editor window title."""
    return domain.find_article_from_title(
        ui.active_window().title, note_config.article_library_dir()
    )


def _current_article_notes_path() -> Path | None:
    """Return the current article's notes path, or notify if unavailable."""
    article_path = _find_article_from_title()
    if not article_path:
        app.notify("Article Notes", "Not viewing a library article")
        actions.user.play_thunk()
        return None
    return domain.ensure_notes_file(article_path)


def _selected_or_expanded_text(max_expands: int = 3) -> str:
    """Return selected text, expanding semantic selection in Cursor if needed."""
    selected = actions.edit.selected_text()
    if selected and selected.strip():
        return selected

    for _ in range(max_expands):
        actions.user.vscode("editor.action.smartSelect.expand")
        actions.sleep("80ms")
        selected = actions.edit.selected_text()
        if selected and selected.strip():
            return selected

    return ""


_get_article_title = domain.get_article_title
_notes_path_for = domain.notes_path_for
_ensure_notes_file = domain.ensure_notes_file
_add_tag = domain.add_tag
_normalize_excerpt = domain.normalize_excerpt
_append_excerpt = domain.append_excerpt
_append_timestamped_note = domain.append_timestamped_note


@mod.action_class
class Actions:
    def article_copy_to_notes():
        """Copy selected text from a journal article to its notes file."""
        selected = actions.edit.selected_text()
        if not selected or not selected.strip():
            app.notify("Article Notes", "No text selected")
            actions.user.play_thunk()
            return

        notes_path = _current_article_notes_path()
        if not notes_path:
            return
        _append_excerpt(notes_path, selected)
        actions.user.play_ding()

    def article_tag(tag: str):
        """Add a tag to the current article's notes file."""
        notes_path = _current_article_notes_path()
        if not notes_path:
            return
        if _add_tag(notes_path, tag):
            actions.user.play_ding()
            app.notify("Article Notes", f"Tagged: #{tag}")
        else:
            app.notify("Article Notes", f"Already tagged: #{tag}")

    def article_add_note(text: str):
        """Append a dictated note to the current article's notes file."""
        notes_path = _current_article_notes_path()
        if not notes_path:
            return
        _append_timestamped_note(notes_path, text)
        actions.user.play_ding()

    def article_open_notes():
        """Open the notes file for the current article in Cursor."""
        notes_path = _current_article_notes_path()
        if not notes_path:
            return
        open_path_in_macos_app("Cursor", notes_path)
        actions.user.play_ding()

    def article_capture_sentence_to_notes():
        """Capture current sentence-ish selection in Cursor and append to article notes."""
        notes_path = _current_article_notes_path()
        if not notes_path:
            return
        selected = _selected_or_expanded_text()
        if not selected or not selected.strip():
            app.notify("Article Notes", "Could not capture sentence at cursor")
            actions.user.play_thunk()
            return

        _append_excerpt(notes_path, selected)
        actions.user.play_ding()
        app.notify("Article Notes", f"Captured excerpt to {notes_path.name}")
