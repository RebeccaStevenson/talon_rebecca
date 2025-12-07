# Basic Usage

The examples below are just a very small selection of common commands for working with Talon. These are based on the [Talon Community](https://github.com/talonhub/community) user file set.

## Mode Switching

Talon has three basic modes by default:

- In **command mode**, your speech will be interpreted as commands by default.
- In **dictation mode**, your speech will be transcribed as plain text by default (although with some commands, like "comma" etc. for punctuation), similar to traditional speech recognition systems.
- In **sleep mode**, Talon will do nothing until it hears a commands that wakes it up.

To keep track of what mode you are in with a visual icon, enable the [mode indicator feature](https://github.com/talonhub/community/tree/main/plugin/mode_indicator) in the community repository.

| Command          | Description                 |
| ---------------- | --------------------------- |
| `wake up`        | Enable speech recognition.  |
| `go to sleep`    | Disable speech recognition. |
| `dictation mode` | Switch to dictation mode.   |
| `command mode`   | Switch to command mode.     |

## Help Commands

| Command                      | Description                                                      |
| ---------------------------- | ---------------------------------------------------------------- |
| `help alphabet`              | show the spelling alphabet for pressing individual keys          |
| `help context`               | show all defined commands                                        |
| `help active`                | show all currently available commands                            |
| `help next`, `help previous` | go to the next or previous page of help items if there are a lot |
| `help close`                 | hide any open help window again                                  |
| `command history`            | show the command history                                         |
| `talon open log`             | open the Talon log for debugging                                 |

## Dictating Text

Say a formatter then the text. (i.e. `say "hello world"`) to dictate while in command mode

| Formatter         | Description                             |
| ----------------- | --------------------------------------- |
| `say`             | no special formatting is applied        |
| `sentence`        | the first word is capitalized           |
| `title`           | every word starts with a capital letter |
| `all down`        | every word is all lower case            |
| `smash`           | no spaces between words                 |
| `kebab`           | dashes instead of spaces                |
| `help formatters` | show all available formatters           |

## Customize Talon

These commands will open up a CSV or [Talon list](Customization/talon_lists.md) file in your default text editor that you can edit to customize voice commands without needing to write Talon scripts.

| Command                      | Description                                       |
| ---------------------------- | ------------------------------------------------- |
| `customize additional words` | add additional words that Talon will recognize    |
| `customize words to replace` | remap or reformat words that Talon will recognize |
| `customize alphabet`         | change the default Talon alphabet                 |
| `customize websites`         | add websites that can be opened with Talon        |

## Working with applications

| Command             | Description                                                       |
| ------------------- | ----------------------------------------------------------------- |
| `focus "app name"`  | say "focus chrome" for example, to switch active window to chrome |
| `running list`      | see all active applications                                       |
| `launch "app name"` | say "launch chrome" for example, to open chrome                   |
| `window close`      | closes the currently active window                                |

## Working with tabs

| Command           |
| ----------------- |
| `tab new`         |
| `tab last`        |
| `tab next`        |
| `tab close`       |
| `tab restore`     |
| `go tab <number>` |
| `go tab final`    |

## Working with media

| Command         |
| --------------- |
| `mute`          |
| `play next`     |
| `play previous` |
| `play`          |

## Controlling the Tobii eye tracker

| Commands          | Description                          |
| ----------------- | ------------------------------------ |
| `run calibration` | start Tobii calibration              |
| `control mouse`   | toggle on/off Tobii moving the mouse |
| `zoom mouse`      | Toggle Control Mouse (Zoom).         |
| `control off`     | Turn the eye tracker off             |

## Working with text

| Command        | Description                                                               |
| -------------- | ------------------------------------------------------------------------- |
| `copy that`    |                                                                           |
| `control cap`  | copy via the keyboard shortcut using the Talon alphabet (`cap` for `c`)   |
| `paste that`   |                                                                           |
| `control vest` | paste via the keyboard shortcut using the Talon alphabet (`vest` for `v`) |
| `cut that`     |                                                                           |
| `undo that`    |                                                                           |
| `redo that`    |                                                                           |
| `scratch that` | undo Talon dictation                                                      |

## Mouse Commands

| Command      | Description                             |
| ------------ | --------------------------------------- |
| `touch`      | single click                            |
| `duke`       | double click                            |
| `trip click` | triple click                            |
| `drag`       | hold down the mouse. Repeat to release  |
| `curse yes`  | hides the mouse cursor for eye tracking |
| `curse no`   | shows the mouse cursor                  |
| `righty`     | right click                             |

## Scrolling

| Command        | Description                            |
| -------------- | -------------------------------------- |
| `page down`    | press the page down key                |
| `page up`      | press the page up key                  |
| `scroll down`  | scroll down                            |
| `scroll up`    | scroll up                              |
| `wheel down`   | scroll down                            |
| `wheel up`     | scroll up                              |
| `wheel left`   | scroll left                            |
| `wheel gaze`   | scroll according to the mouse position |
| `wheel upper`  | continually scroll up                  |
| `wheel downer` | continually scroll down                |
| `wheel stop`   | stop scrolling                         |



================================================
FILE: docs/Basic Usage/settings.md
================================================
# Settings

Talon's behavior can be changed by changing the value of settings within a `.talon` file inside a `settings():` block.

```talon
# Example Talon file
settings():
    # Enable the Talon mode indicator
    user.mode_indicator_show = true
```

:::tip

Talon settings can be applied from any `.talon` file in the user directory, regardless of the filename or location.

:::

:::important

If the same setting is defined multiple times, Talon will use the setting value in the `.talon` file with the most specific context match.

:::

## Community Settings

| Setting                              | Example Value | Description                                                                                                                                             |
| ------------------------------------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| user.file_manager_auto_show_pickers  | false         | If `true`, automatically show the picker GUI when the file manager has focus                                                                            |
| user.help_max_command_lines_per_page | 50            | Set the number of command lines to display per help page                                                                                                |
| user.help_max_contexts_per_page      | 20            | Set the number of contexts to display per help page                                                                                                     |
| user.mouse_continuous_scroll_amount  | 80            | Set the scroll amount for continuous scroll/gaze scroll                                                                                                 |
| user.mouse_enable_pop_stops_scroll   | true          | If `true`, stop continuous scroll/gaze scroll with a pop                                                                                                |
| user.mouse_enable_pop_click          | 1             | Choose how pop click should work in 'control mouse' mode (0 = off, 1 = on with eyetracker but not zoom mouse mode, 2 = on but not with zoom mouse mode) |
| user.mouse_enable_hiss_scroll        | false         | If `true`, use a hissing noise to scroll continuously                                                                                                   |
| user.mouse_hide_mouse_gui            | false         | If `true`, hide the continuous scroll/gaze scroll GUI                                                                                                   |
| user.mouse_wake_hides_cursor         | false         | If `true`, hide the cursor when enabling zoom mouse                                                                                                     |
| user.mouse_wheel_down_amount         | 120           | Set the amount to scroll up/down                                                                                                                        |
| user.mouse_wheel_horizontal_amount   | 40            | Set the amount to scroll left/right                                                                                                                     |
| user.grids_put_one_bottom_left       | true          | If `true`, start mouse grid numbering on the bottom left (vs. top left)                                                                                 |
| user.command_history_display         | 10            | Set the default number of command history lines to display                                                                                              |
| user.command_history_size            | 50            | Set the total number of command history lines to display                                                                                                |
| user.mode_indicator_show             | false         | Enable the mode indicator                                                                                                                               |
| user.mode_indicator_x                | 1             | X Position for the mode indicator when it is enabled                                                                                                    |
| user.mode_indicator_y                | 0             | Y Position for the mode indicator when it is enabled                                                                                                    |
| user.listening_timeout_minutes       | 3             | Puts Talon into sleep mode if no commands are spoken for a defined period of time.                                                                      |

## Core Talon Settings

| Setting         | Example Value | Description                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| imgui.scale     | 1.5           | Adjust the scale of the imgui windows                                                                                                                                                                                                                                                                                                                                                         |
| imgui.dark_mode | false         | If `true` enable dark mode for Talon imgui menus (used for help menus in community)                                                                                                                                                                                                                                                                                                           |
| insert_wait     | 0             | Increase this if characters seem to be jumbled in a specific app when typing whole sentences. Default is 0.                                                                                                                                                                                                                                                                                   |
| key_hold        | 16            | Increase this if you're playing a game and some keys aren't registering at all. You should probably increase it in 16ms increments, e.g. set it to 16ms or 32ms.                                                                                                                                                                                                                              |
| key_wait        | 1             | Increase this if modifier keys are getting dropped or if key presses are misbehaving even with the other two settings (`insert_wait` and `key_hold`) tuned. `key_wait` should be the last resort because it results in the slowest overall keypress rate. Default is 1.0 in milliseconds.                                                                                                     |
| speech.engine   |               | Determines which [speech engine](../Resource%20Hub/Speech%20Recognition/speech%20engines.md) Talon uses to recognize input. This is useful for configuring dictation mode to use a different speech engine; for example, 'webspeech'.                                                                                                                                                         |
| speech.timeout  |               | This determines how long a pause Talon waits for before deciding you've finished speaking and interpreting what you've just said as a sequence of commands. This parameter is generally very important; for example, it determines the amount of time you can pause between saying 'phrase' and the following phrase. It is measured in seconds; the default is 0.300, i.e. 300 milliseconds. |

To add your own additional custom settings for changing Talon behavior, see [the settings customization page](../Customization/Talon%20Framework/settings.md)



================================================
FILE: docs/Customization/basic_customization.md
================================================
---
sidebar_position: 1
---

