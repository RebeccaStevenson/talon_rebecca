os: mac
-
# System navigation shortcuts
tab move: key(ctrl-f7)

keyboard access: key(ctrl-f1)

menu focus: key(ctrl-shift-cmd-m)

window next: key(ctrl-f4)

dock focus: key(ctrl-f3)

toolbar focus: key(ctrl-f5)

float focus: key(ctrl-f6)

status focus: key(ctrl-f8)

show menu: key(ctrl-.)

# Restore bare arrow-key presses.
# The old community fork had `<user.arrow_keys>: user.move_cursor(arrow_keys)`
# which mapped up/down/left/right to arrow keys. Fresh upstream removed this.
up: key(up)

down: key(down)

left: key(left)

right: key(right)

# Page up/down — uses edit.page_up()/page_down() so apps can override.
# The old fork had these in core/edit/edit.talon; fresh upstream renamed
# them to "scroll up"/"scroll down". Restoring the old spoken forms here.
upper: edit.page_up()

downer: edit.page_down()

# Mouse scroll commands
go up: user.mouse_scroll_up()

go down: user.mouse_scroll_down()

wheel upper: user.mouse_scroll_continuous("UP")

wheel downer: user.mouse_scroll_continuous("DOWN")
