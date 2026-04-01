# SuperWhisper example shell scripts (macOS)

These are **example** scripts that can live directly in `apps/superwhisper/scripts/` and be referenced by the Talon actions in this folder.

## Quick start

1. Make the scripts executable:

```bash
chmod +x ~/.talon/user/talon_rebecca/apps/superwhisper/scripts/superwhisper_*_mode.sh
```

2. Test one manually:

```bash
~/.talon/user/talon_rebecca/apps/superwhisper/scripts/superwhisper_super_mode.sh
```

## How they work

The scripts use SuperWhisper’s URL scheme:

- `superwhisper://record` starts recording
- `superwhisper://mode?key=<mode_key>` selects a mode by key (as defined in SuperWhisper)

If your mode switch is flaky, try increasing the `sleep` in the scripts.
