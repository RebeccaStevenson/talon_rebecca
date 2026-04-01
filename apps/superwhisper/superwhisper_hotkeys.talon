os: mac
mode: all
-

# Recovery / control hotkeys for the SuperWhisper workflow.
#
# If you start SuperWhisper via `user.whisper_start()`, Talon speech is disabled to prevent conflicts.
# If you later stop SuperWhisper outside Talon (e.g. SuperWhisper UI / its own hotkey),
# Talon will remain disabled until you re-enable it.

key(ctrl-alt-shift-cmd-w):
    app.notify("Talon wake (speech enable)")
    speech.enable()

key(ctrl-alt-shift-cmd-r):
    app.notify("SuperWhisper start (Talon sleep)")
    user.whisper_start()

key(ctrl-alt-shift-cmd-e):
    app.notify("SuperWhisper stop (Talon wake)")
    user.whisper_stop()
