# Ignore repeats that occur as the first element, to stop hallucinated repeats.

^<number>: user.opening_number_action(number)


#<user.file_suffix>: insert(file_suffix)

# We'll want to use this in all sorts of places
#(interrupt | cease): key(ctrl-c)

#cancel: user.cancel()

# Record all voice clips
#settings(): speech.record_all = 1

