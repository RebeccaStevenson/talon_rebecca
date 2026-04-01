# Antigravity voice commands (VS Code fork).
# This file keeps the shared app context and top-level command palette entrypoint.
app: antigravity
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

window reload: user.antigravity("workbench.action.reloadWindow")
window close: user.antigravity("workbench.action.closeWindow")

please [<user.text>]:
    user.antigravity("workbench.action.showCommands")
    insert(user.text or "")
