os: mac
-

deck(page+): key(pageup)

deck(page-): key(pagedown)

deck(Wh+): user.whisper_start()

deck(Wh-): user.whisper_stop()

deck(WhS+): user.whisper_record_mode("super")

deck(WhS-): user.whisper_stop()

deck(Tal+): user.deck_toggle_talon_speech()

deck(SMB): user.audio_input_set_preferred("MacBook Pro Microphone")

deck(SSh): user.audio_input_set_preferred("Shokz Loop110")

deck(TMB): sound.set_microphone("MacBook Pro Microphone")

deck(SMB+):
    user.audio_input_save_current()
    user.audio_input_set_preferred("MacBook Pro Microphone")
    sleep(100ms)
    user.whisper_start()

deck(SR+):
    user.audio_input_restore_saved()
    sleep(100ms)
    user.whisper_start()

deck(TMB+):
    sound.set_microphone("MacBook Pro Microphone")
    sleep(100ms)
    user.whisper_start()

deck(TD+):
    sound.set_microphone("System Default")
    sleep(100ms)
    user.whisper_start()

deck(Again): core.repeat_partial_phrase(1)

deck(Wh- nw): user.whisper_stop(false)
