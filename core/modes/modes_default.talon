# Original author: jcaw
# Source: https://github.com/jcaw/talon_config

# Also register sleep command in the default mode, so it can be chained.
#(snore | sleep)$: user.noisy_sleep()
(snore)$: user.noisy_sleep()
