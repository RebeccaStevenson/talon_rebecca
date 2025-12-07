"""
Antigravity (VS Code fork) configuration for Talon.

This module declares the Antigravity app and provides all the necessary
actions to control Antigravity via voice commands, mirroring the VS Code
functionality.
"""

from talon import Context, Module, actions, app

is_mac = app.platform == "mac"

# Module declaration
mod = Module()

# Declare the antigravity app
mod.apps.antigravity = """
os: mac
and app.name: Antigravity
"""

# Contexts
ctx = Context()
mac_ctx = Context()

ctx.matches = r"""
app: antigravity
"""

mac_ctx.matches = r"""
os: mac
app: antigravity
"""


# Helper function to execute commands via command palette
def execute_command_via_palette(command_id: str, wait: bool = False):
    """Execute a command via the command palette."""
    actions.user.antigravity_command_palette()
    actions.insert(command_id)
    actions.key("enter")
    if wait:
        actions.sleep("100ms")


# Module-level actions (available globally once antigravity is loaded)
@mod.action_class
class Actions:
    def antigravity(command_id: str):
        """Execute command via Antigravity command palette."""
        execute_command_via_palette(command_id, False)

    def antigravity_and_wait(command_id: str):
        """Execute command via Antigravity command palette and wait for it to complete."""
        execute_command_via_palette(command_id, True)

    def antigravity_terminal(number: int):
        """Activate a terminal by number in Antigravity"""
        actions.user.antigravity(f"workbench.action.terminal.focusAtIndex{number}")

    def antigravity_command_palette():
        """Show Antigravity command palette"""
        actions.key("ctrl-shift-p")


# Mac-specific command palette override
@mac_ctx.action_class("user")
class MacUserActions:
    def antigravity_command_palette():
        actions.key("cmd-shift-p")


# App actions for Antigravity context
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


# Code actions for Antigravity context
@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.user.antigravity("editor.action.commentLine")


# Edit actions for Antigravity context
@ctx.action_class("edit")
class EditActions:
    def indent_more():
        actions.user.antigravity("editor.action.indentLines")

    def indent_less():
        actions.user.antigravity("editor.action.outdentLines")

    def save_all():
        actions.user.antigravity("workbench.action.files.saveAll")

    def find(text=None):
        if is_mac:
            actions.key("cmd-f")
        else:
            actions.key("ctrl-f")
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


# Window actions for Antigravity context
@ctx.action_class("win")
class WinActions:
    def filename():
        title = actions.win.title()
        if is_mac:
            result = title.split(" — ")[0]
        else:
            result = title.split(" - ")[0]
        if "." in result:
            return result
        return ""


# User actions for Antigravity context
@ctx.action_class("user")
class UserActions:
    # splits.py support
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

    # multiple_cursor.py support
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

    # snippet.py support
    def snippet_search(text: str):
        actions.user.antigravity("editor.action.insertSnippet")
        actions.insert(text)

    def snippet_insert(text: str):
        """Inserts a snippet"""
        actions.user.antigravity("editor.action.insertSnippet")
        actions.insert(text)
        actions.key("enter")

    def snippet_create():
        """Triggers snippet creation"""
        actions.user.antigravity("workbench.action.openSnippets")

    def tab_jump(number: int):
        if number < 10:
            if is_mac:
                actions.user.antigravity(f"workbench.action.openEditorAtIndex{number}")
            else:
                actions.key(f"alt-{number}")
        else:
            actions.user.antigravity("workbench.action.openEditorAtIndex")
            actions.insert(str(number))
            actions.key("enter")

    def tab_final():
        if is_mac:
            actions.user.antigravity("workbench.action.lastEditorInGroup")
        else:
            actions.key("alt-0")

    def split_number(index: int):
        """Navigates to a the specified split"""
        if index < 9:
            if is_mac:
                actions.key(f"cmd-{index}")
            else:
                actions.key(f"ctrl-{index}")

    # find_and_replace.py support
    def find(text: str):
        """Triggers find in current editor"""
        if is_mac:
            actions.key("cmd-f")
        else:
            actions.key("ctrl-f")
        if text:
            actions.insert(text)

    def find_next():
        actions.user.antigravity("editor.action.nextMatchFindAction")

    def find_previous():
        actions.user.antigravity("editor.action.previousMatchFindAction")

    def find_everywhere(text: str):
        """Triggers find across project"""
        if is_mac:
            actions.key("cmd-shift-f")
        else:
            actions.key("ctrl-shift-f")
        if text:
            actions.insert(text)

    def find_toggle_match_by_case():
        """Toggles find match by case sensitivity"""
        if is_mac:
            actions.key("alt-cmd-c")
        else:
            actions.key("alt-c")

    def find_toggle_match_by_word():
        """Toggles find match by whole words"""
        if is_mac:
            actions.key("cmd-alt-w")
        else:
            actions.key("alt-w")

    def find_toggle_match_by_regex():
        """Toggles find match by regex"""
        if is_mac:
            actions.key("cmd-alt-r")
        else:
            actions.key("alt-r")

    def replace(text: str):
        """Search and replaces in the active editor"""
        if is_mac:
            actions.key("alt-cmd-f")
        else:
            actions.key("ctrl-h")
        if text:
            actions.insert(text)

    def replace_everywhere(text: str):
        """Search and replaces in the entire project"""
        if is_mac:
            actions.key("cmd-shift-h")
        else:
            actions.key("ctrl-shift-h")
        if text:
            actions.insert(text)

    def replace_confirm():
        """Confirm replace at current position"""
        if is_mac:
            actions.key("shift-cmd-1")
        else:
            actions.key("ctrl-shift-1")

    def replace_confirm_all():
        """Confirm replace all"""
        if is_mac:
            actions.key("cmd-enter")
        else:
            actions.key("ctrl-alt-enter")

    def select_previous_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("shift-enter esc")

    def select_next_occurrence(text: str):
        actions.edit.find(text)
        actions.sleep("100ms")
        actions.key("esc")


