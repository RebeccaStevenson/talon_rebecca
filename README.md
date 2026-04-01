# talon_rebecca

Personal Talon command set and compatibility layer on top of upstream Talon/community packages.

See `CONTRIBUTING.md` for placement rules, testing expectations, and the current settings layout.

## Overview

- SuperWhisper handoff commands that cleanly toggle speech control between Talon and SuperWhisper
- Voice shortcuts for Claude, Codex, and ChatGPT
- Overrides related to repetition and key naming

## SuperWhisper Handoff

This repo includes a SuperWhisper integration for switching between Talon command mode and SuperWhisper dictation.

| Command | What it does | Scope | App / reference |
|---|---|---|---|
| `whisper start` | Disables Talon speech and starts SuperWhisper recording | Global | [SuperWhisper](https://superwhisper.com/), [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md) |
| `whisper stop` | Stops SuperWhisper and re-enables Talon speech | Global | [SuperWhisper](https://superwhisper.com/), [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md) |
| `whisper cancel` / `super cancel` | Cancels recording and returns control to Talon | Global | [SuperWhisper](https://superwhisper.com/), [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md) |
| `whisper mode <mode>` | Switches SuperWhisper mode without starting recording | Global | [SuperWhisper](https://superwhisper.com/), [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md) |
| `whisper start <mode>` | Switches mode and starts recording | Global | [SuperWhisper](https://superwhisper.com/), [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md) |

If you want the full setup, mode configuration, and caveats, see [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md).

## AI Tool Commands

### Claude

| Tool | Command | What it does | Scope | App / reference |
|---|---|---|---|---|
| Claude | `claude start` | Launches Claude Code | Global | [Claude](https://www.anthropic.com/claude), `apps/claude/` |
| Claude | `claude start <path>` | Launches Claude Code in a target directory | Global | [Claude](https://www.anthropic.com/claude), `apps/claude/` |
| Claude | `claude yolo` | Launches Claude Code with permissive flags | Global | [Claude](https://www.anthropic.com/claude), `apps/claude/` |
| Claude | `claude allow` | Launches Claude Code with allow-based permissions | Global | [Claude](https://www.anthropic.com/claude), `apps/claude/` |
| Claude | `claude new conversation` | Creates a new conversation in the Claude desktop app | Claude desktop | [Claude](https://www.anthropic.com/claude), `apps/claude/` |
| Claude | `claude open settings` | Opens Claude desktop settings | Claude desktop | [Claude](https://www.anthropic.com/claude), `apps/claude/` |
| Codex | `start codex` | Launches Codex | Global | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex search` | Starts the Codex search flow | Global | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex allow` | Launches Codex with `--full-auto` | Global | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex command menu` | Opens the Codex command palette | Codex desktop | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex reload skills` | Runs the “Force reload skills” command | Codex desktop | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex thread new` | Creates a new thread | Codex desktop | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex open folder` | Opens a folder in Codex | Codex desktop | [Codex](https://openai.com/codex/), `apps/codex/` |
| Codex | `codex toggle terminal` | Toggles the terminal panel | Codex desktop | [Codex](https://openai.com/codex/), `apps/codex/` |
| ChatGPT | `chat new` | Starts a new chat | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |
| ChatGPT | `chat focus` | Focuses the chat input | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |
| ChatGPT | `chat copy` | Copies the current response | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |
| ChatGPT | `chat copy code` | Copies the current code block | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |
| ChatGPT | `chat custom` | Opens the custom instructions shortcut | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |
| ChatGPT | `chat toggle` | Toggles the sidebar or chat panel shortcut | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |
| ChatGPT | `chat trash` | Deletes the current chat | ChatGPT in browser | [ChatGPT](https://chatgpt.com/), `apps/chatgpt/` |

## Additional Commands

| Command | What it does | Notes | App / reference |
|---|---|---|---|
| `homer` / `home row` | Triggers the macOS shortcut bound to `cmd-shift-space` | Can be used inside longer spoken phrases | [Homerow](https://www.homerow.app/), `system/keyboard_mac.talon` |

## Overrides

This repo also includes several overrides to default behavior, for example:

| Override | Behavior in this repo | File | Reference |
|---|---|---|---|
| Bare numbers as repeater | In command mode, small spoken numbers repeat the last partial phrase | `plugin/repeater/repeater_custom.talon` | `plugin/repeater/` |
| Opening-number fallback | Opening numbers are ignored when no context-specific number action is available | `core/opening_numbers.talon` | `core/opening_numbers.py` |
| `backspace` vs `delete` | `backspace` removes left, `delete` means forward delete on macOS | `core/keys/special_keys.py` | `core/keys/` |

### Repeater Behavior

| Spoken form | Result |
|---|---|
| `3` | Repeats the last partial phrase two more times |
| `5` | Repeats the last partial phrase four more times |

## Repository Notes

This repository is for shareable Talon commands, actions, and docs.

Local-only commands and data should live in `~/.talon/user/talon_rebecca_personal/`, not in this repo. Talon will still auto-load that directory because it is under `~/.talon/user/`, but it is outside the `user/talon_rebecca/` git repository.

Keep the following out of `user/talon_rebecca/` unless they are intentionally public:

- custom prompt libraries and text snippets
- absolute local paths
- local vault roots and personal note locations
- personal bookmarks and project-specific URLs
- hardware-specific device names
- personal workflow notes that are not meant for publication

Examples:

- personal prompts/snippets: `~/.talon/user/talon_rebecca_personal/tools/prompts/`
- personal text snippets: `~/.talon/user/talon_rebecca_personal/core/text/`
- local path aliases: `user/talon_rebecca/settings/system_paths-mac.lan.talon-list`

When adding a new command, prefer this rule:

- if it is reusable and safe to publish, keep it in `user/talon_rebecca/`
- if it contains personal content or environment details, put it in `user/talon_rebecca_personal/`

## Import And Test Conventions

Use `user.talon_rebecca...` as the canonical import path for shared modules in both runtime code and pytest.

- prefer `from user.talon_rebecca.core.platform_utils import ...` over repo-root imports like `from core.platform_utils import ...`
- avoid `try/except ImportError` fallbacks for internal repo modules; keep optional imports limited to external platform dependencies
- keep pure logic importable under pytest via the package path configured in `pyproject.toml`
