os: mac
-
# Claude Code keyboard, session, and voice-helper commands.

# Keyboard Shortcuts
claude exit: key(ctrl-d)
claude clear screen: key(ctrl-l)
claude escape edit: key(escape escape)
claude history up: key(up)
claude history down: key(down)
claude tab complete: key(tab)

# Multiline Input
claude line break:
    insert("\\")
    key(enter)
claude multi line: key(option-enter)
claude shift enter: key(shift-enter)
claude control jay: key(ctrl-j)

# Quick Command Prefixes
claude memory: insert("#")
claude slash: insert("/")
claude bash: insert("!")

# Background Commands
claude background: key(ctrl-b)
claude move background: key(ctrl-b)

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
