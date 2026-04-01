os: mac
-
# Claude Code slash-command and vim-mode helpers.

# Slash Commands - Session Management
claude help: insert("/help")
claude exit command: insert("/exit")
claude clear: insert("/clear")
claude config: insert("/config")
claude compact: insert("/compact")
claude resume: insert("/resume")

# Slash Commands - System
claude doctor: insert("/doctor")
claude cost: insert("/cos")
claude ide: insert("/ide")
claude mcp: insert("/mcp")
claude terminal setup: insert("/terminal-setup")
claude permissions: insert("/permissions")

# Vim Mode Commands
claude vim: insert("/vim")
claude vim escape: key(escape)
claude vim insert: insert("i")
claude vim append: insert("a")
claude vim open below: insert("o")
claude vim left: insert("h")
claude vim down: insert("j")
claude vim up: insert("k")
claude vim right: insert("l")
