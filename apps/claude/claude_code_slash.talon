os: mac
-
# Claude Code slash-command and vim-mode helpers.

# Claude-only slash commands.
claude doctor: insert("/doctor")
claude cost: insert("/cost")
claude ide: insert("/ide")
claude terminal setup: insert("/terminal-setup")

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
