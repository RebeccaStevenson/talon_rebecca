# talon_rebecca

Custom Talon command set on top of the upstream Talon community defaults.

See `CONTRIBUTING.md` for placement rules, testing expectations, and the current settings layout.

## Highlighted commands

- SuperWhisper handoff commands that cleanly toggle speech control between Talon and SuperWhisper
- Voice shortcuts for Claude, Codex, and ChatGPT
- Overrides related to repetition and key naming

### SuperWhisper handoff

This repo includes a [SuperWhisper](https://superwhisper.com/) integration for switching between Talon command mode and SuperWhisper dictation.
Reference: [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md).

| Spoken form | Result | Scope |
|---|---|---|
| `whisper start` | Disables Talon speech and starts SuperWhisper recording | Global |
| `whisper stop` | Stops SuperWhisper and re-enables Talon speech | Global |
| `whisper cancel` / `super cancel` | Cancels recording and returns control to Talon | Global |
| `whisper mode <mode>` | Switches SuperWhisper mode without starting recording | Global |
| `whisper start <mode>` | Switches mode and starts recording | Global |

Note: the `normal.json` SuperWhisper mode used with this setup should include an LLM prompt that strips spoken control phrases such as `whisper stop` from the dictated output instead of transcribing them literally.

If you want the full setup, mode configuration, and caveats, see [`apps/superwhisper/superwhisper_talon_integration.md`](apps/superwhisper/superwhisper_talon_integration.md).

### AI tool commands

#### [Claude](https://www.anthropic.com/claude) and [Codex](https://openai.com/codex/)

Related Talon files: [`tools/agents/`](tools/agents/), [`apps/claude/`](apps/claude/), and [`apps/codex/`](apps/codex/).

Codex and Claude share a consolidated agent command layer with an explicit harness prefix. The cheatsheet below follows the compact spoken-form style used by community-generated references: one row per command shape, with placeholders rather than duplicated variants.

##### Launch

| Spoken form | Result | Scope |
|---|---|---|
| `⟨codex | claude⟩ [⟨allow | resume | yolo⟩] [⟨path⟩ [⟨prompt⟩]]` | Launches the selected CLI in the current directory or a target directory; if a prompt follows a path, it seeds the new session; the optional mode maps to the harness-specific flag or subcommand. | Global |

### More commands

#### AI session commands

| Spoken form | Result | Scope |
|---|---|---|
| `⟨codex | claude⟩ cancel` | Sends the interrupt keybinding for the active CLI session. | Terminal / CLI |
| `⟨codex | claude⟩ interrupt` | Sends the interrupt keybinding for the active CLI session. | Terminal / CLI |
| `⟨codex | claude⟩ quit` | Sends the harness-specific quit keybinding. | Terminal / CLI |
| `⟨codex | claude⟩ ⟨clear | compact | diff | help | init | mcp | model | permissions | plan⟩` | Inserts the shared slash command for the selected harness. | Terminal / CLI |
| `⟨codex | claude⟩ slash ⟨clear | compact | diff | help | init | mcp | model | permissions | plan | resume⟩` | Inserts the explicit slash-command form, including `resume`. | Terminal / CLI |
| `codex approvals` | Preserves the older Codex phrase and inserts `/permissions`. | Terminal / CLI |
| `claude doctor` | Inserts the Claude-only `/doctor` slash command. | Terminal / CLI |
| `claude cost` | Inserts the Claude-only `/cost` slash command. | Terminal / CLI |

#### Additional commands

| Spoken form | Result | Notes | Reference |
|---|---|---|---|
| `homer` / `home row` | Triggers the macOS shortcut bound to `cmd-shift-space` | Can be used inside longer spoken phrases | [Homerow](https://www.homerow.app/), `system/keyboard_mac.talon` |

#### AI desktop commands

| Spoken form | Result | Scope |
|---|---|---|
| `codex command menu` | Opens the Codex command palette. | Codex desktop |
| `codex reload skills` | Runs the force-reload-skills command. | Codex desktop |
| `codex thread new` | Creates a new Codex thread. | Codex desktop |
| `codex open folder` | Opens a folder in Codex. | Codex desktop |
| `codex toggle terminal` | Toggles the terminal panel. | Codex desktop |
| `claude new conversation` | Creates a new conversation in the Claude desktop app. | Claude desktop |
| `claude open settings` | Opens Claude desktop settings. | Claude desktop |

## Overrides

This repo also includes several overrides to default behavior, for example:

| Topic | Result | File | Reference |
|---|---|---|---|
| Bare numbers as repeater | In command mode, small spoken numbers repeat the last partial phrase | `plugin/repeater/repeater_custom.talon` | `plugin/repeater/` |
| Opening-number fallback | Opening numbers are ignored when no context-specific number action is available | `core/opening_numbers.talon` | `core/opening_numbers.py` |
| `backspace` vs `delete` | `backspace` removes left, `delete` means forward delete on macOS | `core/keys/special_keys.py` | `core/keys/` |

### Repeater behavior

| Spoken form | Result |
|---|---|
| `⟨phrase⟩ ⟨small number⟩` | Repeats the phrase until the total count matches the spoken number. |
