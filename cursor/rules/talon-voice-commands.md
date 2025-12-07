# Talon Voice Command Guide

## Workspace Layout
Talon loads voice rules from `~/.talon/user`. This repository lives inside that tree, so any `.talon` file here is picked up automatically. Keep platform-agnostic rules under `custom/` unless a tighter scope is required. Existing examples such as `custom/random_mac.talon` demonstrate how to isolate macOS behaviors (`os: mac`) while leaving room for cross-platform files beside them.

## Command File Basics
A `.talon` file pairs spoken phrases with actions. Each file begins with optional context lines, followed by `-` and one command per line. Indentation matters: the first tab or four spaces indent body lines. For instance:
```talon
os: mac
app: code
-
select everything:
    key(ctrl-a)
go down:
    user.mouse_scroll_down()
```
Group related commands together; prefer concise utterances and verbs that match existing naming patterns.

## Adding or Updating Commands
1. Pick the destination file. Extend an existing file when you add a related command, or create `custom/<topic>.talon` for a new feature.
2. Identify the action to call. Search this repository (`rg "scroll down"`) or Talon’s documentation to reuse proven helpers (`user.mouse_scroll_down()`).
3. Define the voice command. Use lowercase phrases, avoid punctuation, and keep modifiers explicit (“go down three”).
4. Test in Talon: reload scripts (`Command+Shift+R` by default) and speak the phrase to confirm the action fires only in the intended context.

## Extending with Python
Complex behaviors often live in Python modules under `custom/`. A module can expose `actions`, `lists`, or `settings` that `.talon` files invoke. When you add a new helper, document the function name in the matching `.talon` file comment or README so others can discover it. Keep functions idempotent and use Talon’s `actions.insert` and `actions.key` helpers instead of raw `subprocess` calls where possible.
