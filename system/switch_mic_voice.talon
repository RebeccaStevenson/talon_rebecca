os: mac
-

# Voice equivalents of Stream Deck microphone-switching buttons.
# Object-verb style per community P01: "mic <target> <device>"
#
# Notification strategy:
#   - System mic/output commands: no pre-notification here; the Python
#     action (SwitchAudioSource wrapper) notifies on success/failure.
#   - Talon mic commands: we notify here because sound.set_microphone()
#     is a built-in with no notification.
#   - Compound commands (whisper): a single summary notification here
#     because the flow involves multiple steps.

# ── System audio input (macOS) ── requires SwitchAudioSource ──

mic system macbook:
    user.audio_set_system_input_macbook()

mic system shokz:
    user.audio_set_system_input_shokz()

# ── Talon speech-recognition microphone ──

mic talon macbook:
    user.audio_set_talon_mic_macbook()

mic talon shokz:
    user.audio_set_talon_mic_shokz()

# ── Combined: set mic + start SuperWhisper ──

mic system macbook whisper:
    user.audio_system_input_macbook_whisper()

mic system restore whisper:
    user.audio_system_input_restore_whisper()

mic talon macbook whisper:
    user.audio_talon_mic_macbook_whisper()

mic talon default whisper:
    user.audio_talon_mic_default_whisper()

# ── Set everything to one device ──

mic all shokz:
    user.audio_set_all_shokz()

mic all macbook:
    user.audio_set_all_macbook()

# ── Audio output only ──
# Sets both macOS system output (via SwitchAudioSource) and Talon output.

output shokz:
    user.audio_set_system_output_shokz()

output macbook:
    user.audio_set_system_output_macbook()
