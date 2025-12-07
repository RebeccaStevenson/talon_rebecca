os: mac
-

deck(page up): key(pageup)
deck(page down): key(pagedown)

deck(whisper start): user.whisper_start()
deck(whisper stop): user.whisper_stop()

deck(talon toggle): user.deck_toggle_talon_speech()

deck(again): core.repeat_partial_phrase(1)
deck(whisper stop don't wake): user.whisper_stop(false)

