# Speaker selection commands
# Provides voice commands for selecting audio output devices

# Show/hide the speaker selection menu
show speakers: user.speaker_selection_toggle()
hide speakers: user.speaker_selection_hide()

# Quick selection of speakers by number
speaker <number_small>: user.speaker_select(number_small)

# Alternative commands
(output|audio) devices: user.speaker_selection_toggle()
change (output|speaker): user.speaker_selection_toggle()
select speaker: user.speaker_selection_toggle() 