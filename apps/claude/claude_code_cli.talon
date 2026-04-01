os: mac
-
# Claude Code CLI invocation, output, and setup helpers.

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

# Installation and Setup
claude install: insert("curl -sL https://install.anthropic.com | sh")
claude setup terminal: insert("/terminal-setup")
