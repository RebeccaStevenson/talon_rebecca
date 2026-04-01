"""App, edit, and user actions for Antigravity."""

from talon import Context, Module, actions, app

from user.talon_rebecca.apps.antigravity.antigravity_helpers import (
    find_everywhere_shortcut,
    find_shortcut,
    replace_confirm_all_shortcut,
    replace_confirm_shortcut,
    replace_everywhere_shortcut,
    replace_shortcut,
    title_to_filename,
    toggle_match_case_shortcut,
    toggle_match_regex_shortcut,
    toggle_match_word_shortcut,
)

mod = Module()
ctx = Context()

ctx.matches = r"""
app: antigravity
"""


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.user.antigravity("workbench.action.files.newUntitledFile")

    def tab_close():
        actions.user.antigravity("workbench.action.closeActiveEditor")

    def tab_next():
        actions.user.antigravity("workbench.action.nextEditorInGroup")

    def tab_previous():
        actions.user.antigravity("workbench.action.previousEditorInGroup")

    def tab_reopen():
        actions.user.antigravity("workbench.action.reopenClosedEditor")

    def window_close():
        actions.user.antigravity("workbench.action.closeWindow")

    def window_open():
        actions.user.antigravity("workbench.action.newWindow")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.user.antigravity("editor.action.commentLine")


@ctx.action_class("edit")
class EditActions:
    def indent_more():
        actions.user.antigravity("editor.action.indentLines")

    def indent_less():
        actions.user.antigravity("editor.action.outdentLines")

    def save_all():
        actions.user.antigravity("workbench.action.files.saveAll")

    def find(text=None):
        actions.key(find_shortcut(app.platform))
        if text is not None:
            actions.insert(text)

    def line_swap_up():
        actions.key("alt-up")

    def line_swap_down():
        actions.key("alt-down")

    def line_clone():
        actions.key("shift-alt-down")

    def line_insert_down():
        actions.user.antigravity("editor.action.insertLineAfter")

    def line_insert_up():
        actions.user.antigravity("editor.action.insertLineBefore")

    def jump_line(n: int):
        actions.user.antigravity("workbench.action.gotoLine")
        actions.insert(str(n))
        actions.key("enter")
        actions.edit.line_start()


@ctx.action_class("win")
class WinActions:
    def filename():
        return title_to_filename(actions.win.title(), app.platform)


@ctx.action_class("user")
class UserActions:
    def split_clear_all():
        actions.user.antigravity("workbench.action.editorLayoutSingle")

    def split_clear():
        actions.user.antigravity("workbench.action.joinTwoGroups")

    def split_flip():
        actions.user.antigravity("workbench.action.toggleEditorGroupLayout")

    def split_maximize():
        actions.user.antigravity("workbench.action.maximizeEditor")

    def split_reset():
        actions.user.antigravity("workbench.action.evenEditorWidths")

    def split_last():
        actions.user.antigravity("workbench.action.focusLeftGroup")

    def split_next():
        actions.user.antigravity_and_wait("workbench.action.focusRightGroup")

    def split_window_down():
        actions.user.antigravity("workbench.action.moveEditorToBelowGroup")

    def split_window_horizontally():
        actions.user.antigravity("workbench.action.splitEditorOrthogonal")

    def split_window_left():
        actions.user.antigravity("workbench.action.moveEditorToLeftGroup")

    def split_window_right():
        actions.user.antigravity("workbench.action.moveEditorToRightGroup")

    def split_window_up():
        actions.user.antigravity("workbench.action.moveEditorToAboveGroup")

    def split_window_vertically():
        actions.user.antigravity("workbench.action.splitEditor")

    def split_window():
        actions.user.antigravity("workbench.action.splitEditor")

    def multi_cursor_add_above():
        actions.user.antigravity("editor.action.insertCursorAbove")

    def multi_cursor_add_below():
        actions.user.antigravity("editor.action.insertCursorBelow")

    def multi_cursor_add_to_line_ends():
        actions.user.antigravity("editor.action.insertCursorAtEndOfEachLineSelected")

    def multi_cursor_disable():
        actions.key("escape")

    def multi_cursor_enable():
        actions.skip()

    def multi_cursor_select_all_occurrences():
        actions.user.antigravity("editor.action.selectHighlights")

    def multi_cursor_select_fewer_occurrences():
        actions.user.antigravity("cursorUndo")

    def multi_cursor_select_more_occurrences():
        actions.user.antigravity("editor.action.addSelectionToNextFindMatch")

    def multi_cursor_skip_occurrence():
        actions.user.antigravity("editor.action.moveSelectionToNextFindMatch")

    def snippet_search(text: str):
        actions.user.antigravity("editor.action.insertSnippet")
        actions.insert(text)

    def snippet_insert(text: str):
        """Insert a snippet."""
        actions.user.antigravity("editor.action.insertSnippet")
        actions.insert(text)
        actions.key("enter")

    def snippet_create():
        """Trigger snippet creation."""
        actions.user.antigravity("workbench.action.openSnippets")

    def tab_jump(number: int):
        if number < 10:
            if app.platform == "mac":
                actions.user.antigravity(f"workbench.action.openEditorAtIndex{number}")
            else:
                actions.key(f"alt-{number}")
        else:
            actions.user.antigravity("workbench.action.openEditorAtIndex")
            actions.insert(str(number))
            actions.key("enter")

    def tab_final():
        if app.platform == "mac":
            actions.user.antigravity("workbench.action.lastEditorInGroup")
        else:
            actions.key("alt-0")

    def split_number(index: int):
        """Navigate to the specified split."""
        if index < 9:
            if app.platform == "mac":
                actions.key(f"cmd-{index}")
            else:
                actions.key(f"ctrl-{index}")

    def find(text: str):
        """Trigger find in the current editor."""
        actions.key(find_shortcut(app.platform))
        if text:
            actions.insert(text)

    def find_next():
        actions.user.antigravity("editor.action.nextMatchFindAction")

    def find_previous():
        actions.user.antigravity("editor.action.previousMatchFindAction")

    def find_everywhere(text: str):
        """Trigger find across the project."""
        actions.key(find_everywhere_shortcut(app.platform))
        if text:
            actions.insert(text)

    def find_toggle_match_by_case():
        """Toggle match by case sensitivity."""
        actions.key(toggle_match_case_shortcut(app.platform))

    def find_toggle_match_by_word():
        """Toggle match by whole words."""
        actions.key(toggle_match_word_shortcut(app.platform))

    def find_toggle_match_by_regex():
        """Toggle match by regex."""
        actions.key(toggle_match_regex_shortcut(app.platform))

    def replace(text: str):
        """Search and replace in the active editor."""
        actions.key(replace_shortcut(app.platform))
        if text:
            actions.insert(text)

    def replace_everywhere(text: str):
        """Search and replace in the entire project."""
        actions.key(replace_everywhere_shortcut(app.platform))
        if text:
            actions.insert(text)

    def replace_confirm():
        """Confirm replace at the current position."""
        actions.key(replace_confirm_shortcut(app.platform))

    def replace_confirm_all():
        """Confirm replace all."""
        actions.key(replace_confirm_all_shortcut(app.platform))

    def select_previous_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("shift-enter esc")

    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("esc")
