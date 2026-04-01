os: mac
-

# macOS *system* audio input switching.
# Requires SwitchAudioSource (brew install switchaudio-osx).
switch audio input: user.switch_audio_input()
system input close: user.system_input_selection_hide()
system input <number_small>: user.system_input_select(number_small)

