mode: command
-
# Make bare numbers resolve to repeat in command mode instead of the generic
# opening-number handler while still allowing additional commands in the same
# utterance after the repeat count.
<number_small>: user.repeat_trailing_number(number_small - 1)

# parrot(click): core.repeat_phrase(1)
key(ctrl-alt-shift-cmd-t): core.repeat_phrase(1)


    
