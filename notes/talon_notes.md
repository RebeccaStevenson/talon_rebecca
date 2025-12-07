# Talon Notes

## Microphone selection commands
- `microphone show`: Displays the microphone picker overlay. Defined in `community/plugin/microphone_selection/microphone_selection.talon`.
- `microphone close`: Hides the picker without changing the current microphone. Same file as above.
- `microphone pick <number_small>`: Selects the numbered microphone shown in the overlay. Speak the number that appears next to the desired device.

## Using key bindings instead of voice commands
- You can trigger any Talon action from a key binding by declaring it the same way you would a voice command, but using the `key(...)` rule. The handlers declared under the rule run when the shortcut is pressed.
- Example (`talon_rebecca/hotkeys.talon`):

```talon
key(ctrl-alt-shift-cmd-u):
    user.hotkey_talon_sleep()
```

- Replace the shortcut inside `key(...)` with the keys you want to bind (e.g. `key(cmd-shift-m)`) and call the desired actions inside the block.
- Additional binding example (`talon_rebecca/core/modes/superwhisper.talon:11`):

```talon
key(ctrl-alt-cmd-p): user.hotkey_talon_sleep()
```
