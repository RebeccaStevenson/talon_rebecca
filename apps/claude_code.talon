os: mac
-
# Claude Code CLI Launch Commands
claude start [<user.system_path>]:
    user.launch_claude_cli(system_path)
claude launch [<user.system_path>]:
    user.launch_claude_cli(system_path)
start claude [<user.system_path>]:
    user.launch_claude_cli(system_path)
claude with prompt: insert("claude \"")

# Keyboard Shortcuts
claude cancel: key(ctrl-c)
claude exit: key(ctrl-d)
claude clear screen: key(ctrl-l)
claude escape edit: key(escape escape)
claude history up: key(up)
claude history down: key(down)
claude tab complete: key(tab)

# Multiline Input
claude line break: insert("\\") key(enter)
claude multi line: key(option-enter)
claude shift enter: key(shift-enter)
claude control jay: key(ctrl-j)

# Quick Command Prefixes
claude memory: insert("#")
claude slash: insert("/")
claude bash: insert("!")

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

# CLI Commands with Arguments
claude version: insert("claude --version")
claude update: insert("claude update")
claude model sonnet: insert("claude --model sonnet")
claude model opus: insert("claude --model opus")
claude model four: insert("claude --model claude-sonnet-4-20250514")
claude continue: insert("claude --continue")
claude resume session: insert("claude -r \"")

# Output Formatting
claude json output: insert("claude -p \"query\" --output-format json")
claude text output: insert("claude -p \"query\" --output-format text")
claude stream json: insert("claude -p \"query\" --output-format stream-json")

# Background Commands
claude background: key(ctrl-b)
claude move background: key(ctrl-b)

# Installation and Setup
claude install: insert("curl -sL https://install.anthropic.com | sh")
claude setup terminal: insert("/terminal-setup")

# File Operations
claude drag file: insert("# Hold Shift while dragging to reference files")
claude tab complete file: key(tab)

# VS Code Integration
claude vs code: insert("# Use cmd+ctrl+shift+4 for screenshot, then ctrl+v to paste")

# Session Navigation
claude previous: key(up)
claude next: key(down)
claude jump back: key(escape escape)

# Special Features
claude screenshot: insert("# cmd+ctrl+shift+4 then ctrl+v (not cmd+v)")
claude paste image: key(ctrl-v)
claude shift drag: insert("# Hold Shift while dragging files")

# Voice Helpers
((claude | clipboard | codex) stop read):
    user.stop_claude_voice_playback()
claude read last:
    user.read_claude_last_response()
codex read last:
    user.read_codex_last_response()
clipboard read:
    user.read_clipboard_text_aloud()
