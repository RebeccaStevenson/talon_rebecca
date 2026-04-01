mode: all
os: mac
-
(whisper) start: user.whisper_start()
(whisper) stop: user.whisper_stop()
(super | whisper) mode: user.whisper_toggle_mode()
(super | whisper) cancel: user.whisper_cancel()

whisper local: user.whisper_local()
whisper normal: user.whisper_normal()
whisper super: user.whisper_super() 

# Generic mode start (doesn't require per-mode shell scripts; extend via superwhisper_mode_key.talon-list)
whisper start {user.superwhisper_mode_key}: user.whisper_record_mode(superwhisper_mode_key)

# Set a specific mode without starting recording (more specific than "whisper mode", so it won't conflict)
whisper mode {user.superwhisper_mode_key}: user.whisper_set_mode(superwhisper_mode_key)
key(ctrl-alt-cmd-y): user.hotkey_talon_sleep()
