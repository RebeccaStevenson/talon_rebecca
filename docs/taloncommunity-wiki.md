# Talon Community Customization Playbook

This condensed wiki is aimed at an agent tasked with tailoring the Talon Community user file set. It summarizes the critical structure, practices, and references required to modify Talon voice automations safely.

---

## 1. Repository Orientation
- `~/.talon/user/community/` (this repo) mirrors upstream Talon Community scripts; keep this directory clean of personal edits when possible.
- `custom/` is ignored by git and is the preferred location for agent-authored overrides, additions, or experiments.
- `plugin/`, `core/`, and `apps/` contain shipped community grammars. Reference these files; avoid editing them directly unless contributing upstream.
- Important doc sources:
  - `docs/Basic Usage/` — end-user command references.
  - `docs/Customization/` — framework, `.talon`, and Python internals.
  - `docs/Help/` — FAQ, Slack guide, beta info.
  - `docs/Integrations/` & `docs/Resource Hub/` — hardware and tooling recommendations.

---

## 2. Agent Workflow Checklist
1. **Sync & Backup**
   - Pull upstream changes (`git pull`).
   - Snapshot current state (`git status`, optional `git stash` or branch).
2. **Define Goal**
   - Clarify target automation, application coverage, and speech patterns.
3. **Plan Placement**
   - Prefer `custom/` mirrors (e.g., `custom/apps/<app>.talon`, `custom/<topic>.py`).
   - If overriding core rules, copy the relevant file into `custom/` and adjust there (higher priority in Talon’s load order).
4. **Implement & Test**
   - Use `.talon` files for command-to-action mappings.
   - Use `.py` for logic, helpers, dynamic lists, and reusable actions under `actions.user.*`.
   - Validate via Talon REPL and voice tests.
5. **Document**
   - Comment non-obvious logic.
   - Update `custom/docs/` summaries or link to relevant docs here.
6. **Review & Deliver**
   - Run edge-case scenarios, confirm context scoping, ensure there are no stray prints/log noise.
   - Provide diffs or summary for hand-off; avoid committing unless instructed.

---

## 3. Voice Command Basics (Reference)
- Default modes: `command`, `dictation`, `sleep`. Use `wake up`, `go to sleep`, `dictation mode`, `command mode`.
- Discoverability commands: `help alphabet`, `help active`, `help context`, `help formatters`, `command history`, `talon open log`.
- Built-in formatters (usable inside rules): `say`, `sentence`, `title`, `all down`, `smash`, `kebab`, etc.
- Common automation phrases (validate when adding overrides):
  - App focus: `focus "app"`, `running list`, `launch "app"`, `window close`.
  - Tabs: `tab new/next/last/close/restore`, `go tab <number|final>`.
  - Editing: `copy that`, `paste that`, `cut that`, `undo that`, `redo that`, `scratch that`.
  - Mouse: `touch`, `duke`, `drag`, `righty`, `curse yes/no`.
  - Scrolling: `scroll up/down`, `wheel upper/downer`, `wheel stop`, `wheel gaze`.
  - Tobii: `run calibration`, `control mouse`, `zoom mouse`, `control off`.

Keep compatibility unless intentionally redesigning workflows.

---

## 4. Settings Overview
- Settings live inside `settings():` blocks in `.talon` files. The most specific context wins.
- Common community overrides: cursor behavior (`user.mouse_*`), history (`user.command_history_columns`), dictation spacing (`user.auto_format_*`), key press delays (`user.key_wait / user.key_hold / user.key_release_wait`), speech tuning (`speech.engine`, `speech.timeout`).
- Example template:

```talon
settings():
    user.wake_word = "talon"
    speech.timeout = 0.4
```

- Reference: `docs/Basic Usage/settings.md` for tables and default values; `docs/Customization/Talon Framework/settings.md` for context precedence tips.

---

## 5. Building Blocks
- **.talon files**: Map spoken rules to actions, tags, modes, lists, or settings. Structure:
  - *Context header* (matchers, tags, apps) above `-` separator.
  - *Body* with rules (`spoken phrase: action.sequence()`), `tag()`, `settings()`, list activations.
- **Python modules (`.py`)**: Implement actions, dynamic lists, events. Organize with `Module()` and `Context()` objects. Example:

```python
from talon import Module, Context, actions

mod = Module()
mod.tag("custom_browser")

ctx = Context()
ctx.matches = r"app: chrome"

@ctx.action_class("user")
class UserActions:
    def go_home():
        actions.key("cmd-l")
        actions.insert("https://talon.wiki")
        actions.key("enter")
```

- **Actions**: Extend via `actions.user.*`; override per-context with `@ctx.action_class`.
- **Lists**: Static via `.talon-list` or inline YAML, dynamic via Python functions returning dicts. Example list injection:

```python
from talon import Module
import json

mod = Module()

@mod.capture(rule="favorite (repo|docs)")
def favorite_resource(m) -> str:
    return {"repo": "https://github.com/talonhub/community", "docs": "https://talon.wiki"}[m[1]]
```

- **Captures**: Convert phrases to structured data; define with `@mod.capture` and reference as `<user.capture_name>` in rules.
- **Modes & Tags**: Gate command availability. Activate with `tag()` in `.talon` or `ctx.tags` in Python. Define custom modes via `mod.mode("my_mode")`.
- **Scopes**: Reflect environment state (`code.language`, `win.app`, etc.). Update custom scopes through Python `scope.update()` helpers.

Reference: `docs/Customization/talon-files.md`, `tallon_lists.md`, `Talon Framework/` subdocs.

---

## 6. Tooling & Debugging
- **Talon REPL**: `Scripting -> Open REPL` or `~/.talon/bin/repl`. Evaluate `actions`, inspect contexts, toggle features.
- **Introspection shortcuts**:
  - `sim("command")` — shows which file handles a phrase.
  - `mimic("phrase")` — replays a voice command.
  - `actions.find("string")` — search for actions by name or docstring.
  - `actions.list("prefix")` — list registered actions.
  - `events.tail(noisy=True)` — stream Talon events for debugging.
  - `registry.commands`, `registry.lists`, `registry.tags`, etc. — inspect current state.
- **Logging**: `talon.log` or `talon open log`. Use `print()` cautiously (prefer removing or gating behind settings).
- **Testing tips**:
  - Temporarily add `actions.user.notify()` or `speech.dispatch()` for instrumentation.
  - For Python modules, rely on `cron` timers or event hooks rather than blocking loops.

---

## 7. Common Customization Patterns
- **Override a command**: copy rule to `custom/`, adjust spoken phrase or action, ensure context specificity.
- **Add new shortcuts**: create `custom/hotkeys.talon` with `key(...)` sequences; optionally rate-limit via settings.
- **Application-specific layers**: new `.talon` file with `app: <bundle>` matcher; include tags to reuse existing command sets.
- **Dynamic list from external data**: load JSON/CSV in Python module, update via `ctx.lists["user.list_name"] = {...}` on file change.
- **Push-to-talk**: see `docs/Customization/Examples/push_to_talk.md`; replicate into `custom/` and adapt keys.
- **Canvas & overlays**: `docs/Customization/Examples/canvas.md` and `Talon Framework/canvas` API references.

---

## 8. Integrations & Dependencies
- Recommended companion tools: browser navigation extensions, OS automation utilities, editors (VS Code, Cursorless, etc.) — see `docs/Integrations/`.
- Hardware guidance (mics, Tobii models, OS-specific notes) in `docs/Resource Hub/Hardware/`.
- Accessibility workflows described in `docs/Integrations/accessibility.md` (non-visual use cases, limitations).
- For dictation accuracy improvements, consult `docs/Resource Hub/Speech Recognition/improving_recognition_accuracy.md` and troubleshooting articles.

---

## 9. Troubleshooting Playbook
- **Command ignored**: verify microphone input, check Talon mode, confirm context matchers, inspect list entries, run `sim()`.
- **Wrong action executed**: inspect overlapping contexts (modes/tags/apps), adjust specificity, check `registry.commands` ordering.
- **Recognition issues**: assess audio quality, gain, noise filters, speech engine selection; revisit formatter usage.
- **Crashes / instability**: review recent custom Python changes, comment out new modules, check `talon.log` stack traces, revert to vanilla community set for comparison.
- **Upstream updates break custom code**: diff release notes (see `docs/Help/beta_talon.md`), update API usage, coordinate with maintainers if necessary.

---

## 10. Community & Support
- Slack (#talon_docs, #help, #customization) — join via [talonvoice.com/chat](https://talonvoice.com/chat); etiquette outlined in `docs/Help/talon-slack.md`.
- FAQ & troubleshooting: `docs/Help/FAQ.md`, `docs/Resource Hub/Speech Recognition/troubleshooting.md`.
- Reporting issues or contributing upstream: follow `CODE_OF_CONDUCT.md` and submit PRs/issues to [github.com/talonhub/community](https://github.com/talonhub/community).

---

## 11. Hand-off Guidance
- Package deliverables inside `custom/` with clear filenames.
- Provide a README snippet or doc entry summarizing new commands, contexts, settings, and dependencies.
- Outline regression tests or voice scripts used for validation.
- Coordinate merge or deployment steps (e.g., update Talon, reload scripts) with the requester.

By using this playbook, an agent can evaluate existing functionality, craft precise customizations, and maintain compatibility with the broader Talon Community ecosystem.

