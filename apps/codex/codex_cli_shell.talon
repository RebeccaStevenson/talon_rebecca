os: mac
app: terminal
app: cursor
-

# Codex shell invocation, config, and install helpers.
codex suggest mode: insert("codex --suggest")
codex auto edit mode: insert("codex --auto-edit")
codex full auto mode: insert("codex --full-auto")
codex read only mode: insert("codex --read-only")

codex with image: insert("codex -i ")
codex image flag: insert("codex --image ")
codex multiple images: insert("codex --image img1.png,img2.jpg ")

codex exec: insert("codex exec ")
codex execute: insert("codex exec ")

codex config: insert("~/.codex/config.toml")
codex config path: insert("~/.codex/config.toml")

codex install npm: insert("npm i -g @openai/codex")
codex latest: insert("npm i -g @openai/codex@latest")

codex docs: insert("github.com/openai/codex")
codex github: insert("https://github.com/openai/codex")
