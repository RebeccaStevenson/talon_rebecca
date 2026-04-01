# talon_rebecca

Custom Talon command set on top upstream talon community default commands

See `CONTRIBUTING.md` for placement rules, testing expectations, and the current settings layout.

## Custom commands I find particularly useful

- SuperWhisper handoff commands that cleanly toggle speech control between Talon and SuperWhisper
- Voice shortcuts for Claude, Codex, and ChatGPT
- Overrides related to repetition and key naming

## [SuperWhisper](https://superwhisper.com/) Handoff

This repo includes a [SuperWhisper](https://superwhisper.com/) integration for switching between Talon command mode and SuperWhisper dictation.
Reference: [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md).

| Command | What it does | Scope |
|---|---|---|
| `whisper start` | Disables Talon speech and starts SuperWhisper recording | Global |
| `whisper stop` | Stops SuperWhisper and re-enables Talon speech | Global |
| `whisper cancel` / `super cancel` | Cancels recording and returns control to Talon | Global |
| `whisper mode <mode>` | Switches SuperWhisper mode without starting recording | Global |
| `whisper start <mode>` | Switches mode and starts recording | Global |

If you want the full setup, mode configuration, and caveats, see [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md).

## AI Tool Commands

### [Claude](https://www.anthropic.com/claude), [Codex](https://openai.com/codex/), and [ChatGPT](https://chatgpt.com/)

Related Talon files: [`tools/agents/`](tools/agents/), [`apps/claude/`](apps/claude/), [`apps/codex/`](apps/codex/), and [`apps/chatgpt/`](apps/chatgpt/).

Codex and Claude now share a consolidated agent command layer while preserving explicit harness prefixes. The spoken prefix selects the harness, and the remainder of the phrase routes through shared launch, key, and slash-command mappings.

| Tool | Command | What it does | Scope |
|---|---|---|---|
| Codex / Claude | `codex` / `claude` | Launches the selected harness in the current directory | Global |
| Codex / Claude | `codex <path>` / `claude <path>` | Launches the selected harness in a target directory | Global |
| Codex / Claude | `codex resume` / `claude resume` | Launches the selected harness in resume mode | Global |
| Codex / Claude | `codex allow` / `claude allow` | Launches the selected harness in the configured allow mode | Global |
| Codex / Claude | `codex yolo` / `claude yolo` | Launches the selected harness in its most permissive mode | Global |
| Codex / Claude | `codex compact` / `claude compact` | Inserts the shared `/compact` slash command | Terminal / CLI |
| Codex / Claude | `codex permissions` / `claude permissions` | Inserts the shared permissions slash command | Terminal / CLI |
| Codex / Claude | `codex slash resume` / `claude slash resume` | Inserts the slash-level `/resume` command inside an active session | Terminal / CLI |
| Codex | `codex search` | Starts the Codex search flow | Global |
| Codex | `codex command menu` | Opens the Codex command palette | Codex desktop |
| Codex | `codex reload skills` | Runs the “Force reload skills” command | Codex desktop |
| Codex | `codex thread new` | Creates a new thread | Codex desktop |
| Codex | `codex open folder` | Opens a folder in Codex | Codex desktop |
| Codex | `codex toggle terminal` | Toggles the terminal panel | Codex desktop |
| Claude | `claude doctor` | Inserts the Claude-only `/doctor` slash command | Terminal / CLI |
| Claude | `claude cost` | Inserts the Claude-only `/cost` slash command | Terminal / CLI |
| Claude | `claude new conversation` | Creates a new conversation in the Claude desktop app | Claude desktop |
| Claude | `claude open settings` | Opens Claude desktop settings | Claude desktop |
| ChatGPT | `chat new` | Starts a new chat | ChatGPT in browser |
| ChatGPT | `chat focus` | Focuses the chat input | ChatGPT in browser |
| ChatGPT | `chat copy` | Copies the current response | ChatGPT in browser |
| ChatGPT | `chat copy code` | Copies the current code block | ChatGPT in browser |
| ChatGPT | `chat custom` | Opens the custom instructions shortcut | ChatGPT in browser |
| ChatGPT | `chat toggle` | Toggles the sidebar or chat panel shortcut | ChatGPT in browser |
| ChatGPT | `chat trash` | Deletes the current chat | ChatGPT in browser |

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
