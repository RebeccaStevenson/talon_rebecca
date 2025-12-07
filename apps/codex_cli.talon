os: mac
app: terminal
app: cursor
-

# Codex CLI Launch Commands
codex [<user.system_path>]:
    user.launch_codex_cli(system_path)
codex launch [<user.system_path>]:
    user.launch_codex_cli(system_path)
start codex [<user.system_path>]:
    user.launch_codex_cli(system_path)
codex search [<user.system_path>]:
    user.codex_search(system_path)

# Keyboard Shortcuts
codex cancel: key(ctrl-c)
codex escape: key(escape)
codex last: key(escape escape)
codex quit: key(ctrl-c ctrl-c)
codex interrupt: key(ctrl-c)

codex close window:
    key(ctrl-c ctrl-c)
    sleep(50ms)
    key(cmd-w)

# Slash Commands
codex clear: insert("/clear")
codex diff: insert("/diff")
codex init: insert("/init")
codex approvals: insert("/approvals")
codex model: insert("/model")
codex mode: insert("/mode")
codex compact: insert("/compact")
codex quit command: insert("/quit")

# Advanced Slash Commands with Arguments
codex diff staged: insert("/diff --staged")
codex model mini: insert("/model o4-mini")
codex compact summary: insert("/compact ")

# Mode Switching
codex suggest mode: insert("codex --suggest")
codex auto edit mode: insert("codex --auto-edit")
codex full auto mode: insert("codex --full-auto")
codex read only mode: insert("codex --read-only")

# Image Support Commands
codex with image: insert("codex -i ")
codex image flag: insert("codex --image ")
codex multiple images: insert("codex --image img1.png,img2.jpg ")

# Non-Interactive Execution
codex exec: insert("codex exec ")
codex execute: insert("codex exec ")

# Configuration Commands
codex config: insert("~/.codex/config.toml")
codex config path: insert("~/.codex/config.toml")

# Installation Commands
codex install npm: insert("npm i -g @openai/codex")
codex latest: insert("npm i -g @openai/codex@latest")

# Quick Actions
codex new line: key(ctrl-j)
codex format: key(shift-enter)

# Help and Documentation
codex help: insert("/help")
codex docs: insert("github.com/openai/codex")
codex github: insert("https://github.com/openai/codex")

reversal environment: 
    insert("cd /Users/rebec/localFiles/reversal_python; conda activate reversal_environment")
    key(enter)
