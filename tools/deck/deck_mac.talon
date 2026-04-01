os: mac
-

deck(page+): key(pageup)

deck(page-): key(pagedown)

deck(Wh+): user.whisper_start()

deck(Wh-): user.whisper_stop()

deck(WhS+): user.whisper_record_mode("super")

deck(WhS-): user.whisper_stop()

deck(Tal+): user.deck_toggle_talon_speech()

deck(SMB): user.audio_set_system_input_macbook()

deck(SSh): user.audio_set_system_input_shokz()

deck(TMB): user.audio_set_talon_mic_macbook_quiet()

deck(TSh): user.audio_set_talon_mic_shokz_quiet()

deck(SMB+):
    user.audio_system_input_macbook_whisper_quiet()

deck(SR+):
    user.audio_system_input_restore_whisper_quiet()

deck(TMB+):
    user.audio_talon_mic_macbook_whisper_quiet()

deck(TD+):
    user.audio_talon_mic_default_whisper_quiet()

deck(Again): core.repeat_partial_phrase(1)

deck(Wh- nw): user.whisper_stop(false)
