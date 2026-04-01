# Integrating SuperWhisper with Talon Voice

This guide explains how to use [SuperWhisper](https://superwhisper.com/) alongside Talon for voice dictation. SuperWhisper provides AI-enhanced speech-to-text with LLM post-processing, which complements Talon's command-and-control capabilities.

## Overview

The integration allows you to:
- Start/stop SuperWhisper dictation via Talon voice commands
- Automatically disable Talon's speech recognition while SuperWhisper is active (to prevent conflicts)
- Switch between different SuperWhisper modes (e.g., "normal" vs "local" processing)

## Files Included

> **📁 Direct Links:**
> - [`apps/superwhisper/superwhisper.talon`](https://github.com/RebeccaStevenson/talon_rebecca/blob/master/apps/superwhisper/superwhisper.talon) - Voice commands
> - [`apps/superwhisper/superwhisper_trigger.py`](https://github.com/RebeccaStevenson/talon_rebecca/blob/master/apps/superwhisper/superwhisper_trigger.py) - Python actions
> - [`tools/superwhisper_modes/normal.json`](https://github.com/RebeccaStevenson/talon_rebecca/blob/master/tools/superwhisper_modes/normal.json) - SuperWhisper mode configuration

### 1. `superwhisper.talon` - Voice Commands

This Talon file provides the following voice commands:

| Command | Action |
|---------|--------|
| `whisper start` | Disables Talon speech and starts SuperWhisper recording |
| `whisper stop` | Stops SuperWhisper recording and re-enables Talon speech |
| `whisper cancel` / `super cancel` | Cancels SuperWhisper (sends Escape) and re-enables Talon |
| `whisper mode` / `super mode` | Toggles SuperWhisper's mode (via `Alt+Cmd+U`) |
| `whisper local` | Switches to local processing mode |
| `whisper normal` | Switches to cloud/normal processing mode |
| `whisper super` | Switches to your "super" mode (implementation depends on your setup) |
| `whisper start <mode>` | Starts recording and switches to the specified mode key (see `superwhisper_mode_key.talon-list`) |
| `whisper mode <mode>` | Switches to the specified mode key **without** starting recording (shows a notification) |

### 2. `superwhisper_trigger.py` - Action Definitions

This Python file defines the Talon actions that control SuperWhisper. The key functions are:

- `whisper_start()` - Disables Talon and triggers SuperWhisper's global hotkey (`Alt+Cmd+R`)
- `whisper_stop()` - Stops recording and re-enables Talon
- `whisper_cancel()` - Cancels without submitting and re-enables Talon
- `whisper_record_mode(mode_key)` - Opens SuperWhisper via URL scheme to start recording and set a specific mode key, then disables Talon speech

### 3. `normal.json` - SuperWhisper Custom Mode

This is a custom SuperWhisper mode configuration with prompts tailored for:
- Fixing voice dictation errors (homophones, misrecognitions)
- Interpreting "new line" and "period" as formatting commands
- Removing stop phrases like "whisper stop" from output
- Converting spoken variable/function names to `snake_case`

The mode prompt should explicitly tell the LLM to remove spoken control phrases such as `whisper stop` from the final transcript instead of transcribing them literally.

## Installation

### Step 1: Install the SuperWhisper Mode

1. Locate your SuperWhisper modes directory:
   ```
   ~/Documents/superwhisper/modes/
   ```

2. Copy the `normal.json` file to that directory.

3. Restart SuperWhisper or use the mode switcher to see your new mode.

**SuperWhisper Documentation**: See [SuperWhisper Getting Started](https://superwhisper.com/docs/getting-started) for more details on modes and configuration.

### Step 2: Install the Talon Files

Copy the `apps/superwhisper/` folder to your Talon user directory (e.g., `~/.talon/user/your_custom_folder/apps/superwhisper/`).

Talon will automatically reload when files are added.

### Step 3: Configure SuperWhisper Hotkey

Ensure SuperWhisper's global recording hotkey is set to `Alt+Cmd+R` (the default). You can verify this in SuperWhisper's settings.

## ⚠️ Important Caveats

### Two ways to switch modes: URL scheme (easier) or shell scripts

There are two approaches in this setup, but **the URL scheme is the simplest and recommended option**.

- **URL scheme (easier + recommended)**:
  - Uses SuperWhisper deeplinks directly, no shell scripts required.
  - Examples:
    - `superwhisper://record` starts recording
    - `superwhisper://mode?key=normal` sets a specific mode key
  - Talon commands that use this:
    - `whisper start <mode>` (record + set mode)
    - `whisper mode <mode>` (set mode only, with notification)
  - The available spoken modes are defined in `superwhisper_mode_key.talon-list`. Add entries there to support additional SuperWhisper mode keys.

- **Shell scripts (optional, for custom/complex switching)**:
  - Keep these only if you need AppleScript/UI automation, extra delays, or logging.
  - `whisper local`, `whisper normal`, and `whisper super` can call scripts from `apps/superwhisper/scripts/` if you need that extra control.
  - Example scripts you can copy and adapt live in:
    - `talon_rebecca/apps/superwhisper/scripts/README.md`
    - `talon_rebecca/apps/superwhisper/scripts/superwhisper_mode_template.sh`
    - `talon_rebecca/apps/superwhisper/scripts/superwhisper_{local,normal,super}_mode.sh`

### Talon Speech Handoff

When you say "whisper start", Talon's speech recognition is disabled. This means:
- You **cannot** use Talon commands while SuperWhisper is recording
- You must use the SuperWhisper interface or its hotkey to stop recording
- Once stopped, Talon speech is automatically re-enabled

If something goes wrong and Talon remains disabled, you can:
1. Use SuperWhisper's UI to stop recording, or
2. Press `Alt+Cmd+R` manually to toggle SuperWhisper, or
3. Use Talon's menu bar icon to re-enable speech

## Customization Tips

- Modify the `prompt` field in `normal.json` to customize how the LLM reformats your dictation
- Add `promptExamples` to teach the model specific corrections you want
- Change the `voiceModelID` and `languageModelID` to use different AI models
- Adjust the hotkeys in `superwhisper_trigger.py` if your SuperWhisper setup uses different shortcuts

## Resources

- [SuperWhisper Documentation](https://superwhisper.com/docs/getting-started)
- [SuperWhisper Community Projects](https://superwhisper.com/docs/get-started/community)
- [Talon Community Wiki](https://talon.wiki/)
- [Talon Slack](https://talonvoice.com/chat) - #help channel for questions
