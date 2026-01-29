os: mac
mode: all
-

# macOS *system* audio input device (used by apps like Zoom).
# Requires SwitchAudioSource (brew install switchaudio-osx).
key(ctrl-alt-cmd-1:passive):
    app.notify("System mic -> MacBook Pro Microphone")
    user.audio_input_set_preferred("MacBook Pro Microphone")

key(ctrl-alt-cmd-3:passive):
    app.notify("System mic -> Shokz Loop110")
    user.audio_input_set_preferred("Shokz Loop110")

key(ctrl-alt-cmd-m:passive):
    app.notify("System mic -> MacBook Pro + SuperWhisper")
    user.audio_input_save_current()
    user.audio_input_set_preferred("MacBook Pro Microphone")
    sleep(100ms)
    user.whisper_start()

# Restore previously-saved macOS system input ("system default" for your workflow).
key(ctrl-alt-cmd-s:passive):
    app.notify("System mic -> restore saved + SuperWhisper")
    user.audio_input_restore_saved()
    sleep(100ms)
    user.whisper_start()

# Talon's speech-recognition microphone (does not change macOS system input).
# Update the device string to match what you see under "microphone show".
key(ctrl-alt-cmd-2:passive):
    app.notify("Talon mic -> MacBook Pro Microphone")
    sound.set_microphone("MacBook Pro Microphone")

key(ctrl-alt-cmd-k:passive):
    app.notify("Talon mic -> MacBook Pro + SuperWhisper")
    sound.set_microphone("MacBook Pro Microphone")
    sleep(100ms)
    user.whisper_start()

# Talon mic back to "System Default" + start SuperWhisper.
key(ctrl-alt-cmd-j:passive):
    app.notify("Talon mic -> System Default + SuperWhisper")
    sound.set_microphone("System Default")
    sleep(100ms)
    user.whisper_start()

# Optional fallback hotkeys (uncomment if needed):
# key(ctrl-alt-shift-cmd-m):
#     app.notify("System mic -> MacBook Pro + SuperWhisper")
#     user.audio_input_save_current()
#     user.audio_input_set_preferred("MacBook Pro Microphone")
#     sleep(100ms)
#     user.whisper_start()
#
# key(ctrl-alt-shift-cmd-s):
#     app.notify("System mic -> restore saved + SuperWhisper")
#     user.audio_input_restore_saved()
#     sleep(100ms)
#     user.whisper_start()
#
# key(ctrl-alt-shift-cmd-k):
#     app.notify("Talon mic -> MacBook Pro + SuperWhisper")
#     sound.set_microphone("MacBook Pro Microphone")
#     sleep(100ms)
#     user.whisper_start()
#
# key(ctrl-alt-shift-cmd-j):
#     app.notify("Talon mic -> System Default + SuperWhisper")
#     sound.set_microphone("System Default")
#     sleep(100ms)
#     user.whisper_start()
