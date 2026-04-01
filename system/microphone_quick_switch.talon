os: mac
mode: all
-

# macOS *system* audio input device (used by apps like Zoom).
# Requires SwitchAudioSource (brew install switchaudio-osx).
# No pre-notification here — the Python action notifies on success/failure.
key(ctrl-alt-cmd-1:passive):
    user.audio_set_system_input_macbook()

key(ctrl-alt-cmd-3:passive):
    user.audio_set_system_input_shokz()

key(ctrl-alt-cmd-m:passive):
    user.audio_system_input_macbook_whisper()

# Restore previously-saved macOS system input ("system default" for your workflow).
key(ctrl-alt-cmd-s:passive):
    user.audio_system_input_restore_whisper()

# Talon's speech-recognition microphone (does not change macOS system input).
# Update the device string to match what you see under "microphone show".
key(ctrl-alt-cmd-2:passive):
    user.audio_set_talon_mic_macbook()

key(ctrl-alt-cmd-4:passive):
    user.audio_set_talon_mic_shokz()

key(ctrl-alt-cmd-k:passive):
    user.audio_talon_mic_macbook_whisper()

# Talon mic back to the canonical default device + start SuperWhisper.
key(ctrl-alt-cmd-j:passive):
    user.audio_talon_mic_default_whisper()
