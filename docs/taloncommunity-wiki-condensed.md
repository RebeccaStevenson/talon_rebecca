# Talon Community Wiki (Condensed)

## Project Overview
- `taloncommunity-wiki/` mirrors the upstream Talon Community files alongside docs, examples, and site sources.
- Follow the Contributor Covenant: be inclusive, respectful, and report issues to community@talon.wiki.
- Maintain backups (git or zipped copies) before major upgrades to recover quickly from breaking changes.

## Daily Use Essentials
### Mode & Speech Control
- Core voice modes: `command`, `dictation`, `sleep`; toggle with `wake up`, `go to sleep`, `command mode`, `dictation mode`.
- Enable the optional [mode indicator](https://github.com/talonhub/community/tree/main/plugin/mode_indicator) for visual feedback.

### Built-in Help & Logging
- Discover commands via `help alphabet`, `help active`, `help context`, and navigate pages with `help next/previous`.
- Inspect history with `command history` and open logs using `talon open log` for quick debugging.

### Dictation & Formatting
- Apply formatters (e.g. `say`, `sentence`, `title`, `all down`, `smash`, `kebab`) to control capitalization and spacing.
- View the full formatter list using `help formatters`.

### Quick Customization Commands
- `customize additional words`, `customize words to replace`, `customize alphabet`, `customize websites` edit CSV-backed lists without touching Talon scripts.

### App, Window, and Tab Control
- Switch focus with `focus "app"`, launch apps by name, inspect `running list`, and close windows with `window close`.
- Manage tabs using `tab new/next/last/close/restore`, `go tab <number>`, `go tab final`.

### Media, Text, and Mouse
- Media: `mute`, `play`, `play next`, `play previous`.
- Text editing: `copy that`, `paste that`, `cut that`, `undo that`, `redo that`, `scratch that`; Talon alphabet shortcuts like `control cap` (`ctrl+c`).
- Mouse: `touch`, `duke`, `trip click`, `drag`, `righty`, `curse yes/no` for cursor visibility.
- Scrolling: `scroll up/down`, `page up/down`, `wheel upper/downer`, `wheel stop`, `wheel gaze` for gaze-based scrolling.

### Tobii Eye Tracker
- `run calibration`, `control mouse`, `zoom mouse`, `control off` provide eye-tracking setup and toggles.

## Settings Primer
- Define settings inside a `.talon` file with a `settings():` block; Talon applies the most specific context match.
- Example:

```talon
settings():
    user.mode_indicator_show = true
```

- Core categories include mouse calibration (`user.mouse_enable_snapping`, `user.mouse_wake_hides_cursor`), command behavior (`user.command_history_columns`), number/text recognition, and speech tuning (`speech.engine`, `speech.timeout`).
- Review the detailed tables in `docs/Basic Usage/settings.md` for full lists and recommended ranges.

## Customization Workflow
- Keep upstream `community` files pristine, then:
  - Option A: edit community files directly (fast, but hard to merge).
  - Option B: maintain a sibling folder for personal scripts (**recommended**).
  - Option C: place overrides in `community/custom/` so they stay git-ignored yet version-controlled.
- Back up before updates; Talon user directories often mix multiple file sets (e.g. `community`, `cursorless`, personal folders).

## Authoring `.talon` Files
- `.talon` files map spoken phrases to actions; `.py` files implement reusable behavior.
- Context header (above the `-`) narrows when rules apply; the body contains voice rules, settings, tags, and list activations.
- Rules use captures (`<user.letter>`, `<digits>`) and lists (`{user.application}`) to generate arguments; combine modifiers like `control` + `shift` naturally.
- Common recipes: remap keyboard shortcuts, slow sequential keypresses with `key_wait`, override default voice mappings, add synonyms after locating the target command via `sim("command")`.

## Python, Actions, and Advanced Concepts
- Use Talon REPL (`talon` menu or `~/.talon/bin/repl`) for experimentation and automation.
- Introspection helpers: `sim()`, `mimic()`, `actions.find()`, `actions.list()`, `events.tail()`, `registry.<type>`.
- Key Talon APIs (in `.pyi` stubs) include `ui` for window management, `clip` for clipboard, `cron` for timers, `screen` and `canvas` for overlays, `imgui` for HUDs, `noise` for hiss/pop detection, and `ctrl` for low-level input.
- Extend with local `.venv` if needed, but avoid hard dependencies for shared scripts.

### Framework Building Blocks
- **Actions**: Python functions bound to `actions.user.*`; override per-context as needed.
- **Apps**: Context selectors by executable, bundle, or regex.
- **Captures**: Convert speech fragments to data; prefer captures when dynamic parsing is needed.
- **Lists**: Map words to strings; support dynamic regeneration and selection lists.
- **Modes & Tags**: Toggle behavior sets; switch modes for command/dictation and activate tags to expose context-specific commands.
- **Modules & Contexts**: Group related actions, lists, and settings; contexts combine mode, tag, scope, and app conditions.
- **Scopes**: Reflect editor state (language, selection); update scopes with background jobs (`cron` or `scope.update()`).

## Examples Snapshot
- Canvas overlays: create, draw, freeze, and remove elements for temporary UIs.
- Push-to-talk: start/stop listening around a key press.
- Toggle listening, auto-sleep on start, and other workflow tweaks show how `.talon` and Python cooperate.

## Integrations & Resources
- Accessibility workflows describe non-visual navigation patterns and limitations; start with essential keyboard-driven tools before layering Talon.
- Recommended add-ons cover browser navigation, OS automation, programming editors, and supplemental utilities.
- Hardware advice (mics, eye trackers) and OS-specific notes live under `docs/Resource Hub/Hardware/`.

## Community & Support Channels
- Beta updates include release notes and install instructions (`docs/Help/beta_talon.md`).
- FAQ highlights: command discovery, multilingual support status, accuracy tips, contribution paths, and troubleshooting basics.
- Join the Talon Slack for peer support; read `talon-slack.md` for etiquette and channel guide.

## Troubleshooting Checklist
- When commands fail: confirm microphone input, verify Talon is running and awake, check speech engine selection, confirm correct user file sets, and inspect logs.
- For misfires: evaluate audio quality, gain, mode, and speech models; consult tips on improving recognition accuracy.
- If Talon crashes: capture logs, revert recent custom changes, and test against the vanilla community profile.

