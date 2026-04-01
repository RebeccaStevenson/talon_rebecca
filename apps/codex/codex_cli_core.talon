os: mac
app: terminal
app: cursor
-

# Codex keyboard, window, and in-session editing commands.
codex escape: key(escape)
codex last: key(escape escape)

codex close window:
    key(ctrl-c ctrl-c)
    sleep(50ms)
    key(cmd-w)

codex new line: key(ctrl-j)
codex format: key(shift-enter)
