app: matlab
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.tabs

# Navigation, searching
search: user.matlab_mod("f")
netch | next match: key(f3)
search in files: user.matlab_mod("shift-f")
go line: user.matlab_mod("g")

recenter:
    user.matlab_mod("k")
    user.matlab_mod("c")

[book] mark set: user.matlab_mod("f2")
[book] mark next: key(shift-f2)

# Folding
fold: user.matlab_mod("shift-[")
fold all:
    user.matlab_mod("k")
    user.matlab_mod("1")

unfold: user.matlab_mod("shift-]")
unfold all:
    user.matlab_mod("k")
    user.matlab_mod("j")

# Indentation
decrease indent: user.matlab_mod("[")
increase indent: user.matlab_mod("]")
reindent: user.matlab_mod("i")
no indent: user.matlab_mod("[:7")

end:
    insert("end")
    key(backspace)

# Miscellaneous editing
comment out: user.matlab_mod("r")
uncomment: user.matlab_mod("t")
scoot up: user.matlab_mod("shift-up")
scoot down: user.matlab_mod("shift-down")
ex kets: user.matlab_mod("shift-m")
ex line: user.matlab_mod("l")
ex cope: user.matlab_mod("shift-space")

assign: insert(" = ")
eval: key(f9)
evaluate: key(f9)

# Basic
command: user.matlab_mod("0")
editor: user.matlab_mod("shift-0")
workspace: user.matlab_mod("3")

run:
    user.matlab_mod("shift-0")
    key(f5)

stop script:
    user.matlab_mod("0")
    user.matlab_mod("c")

# Debugging
debug start:
    user.matlab_mod("0")
    insert("dbstop if error")
    key(enter)

debug clear:
    user.matlab_mod("0")
    insert("dbclear all")
    key(enter)

debug stopper: key(shift-f5)
breakpoint: key(f12)
disable breakpoint: user.matlab_mod("shift-b")
clear breakpoints: user.matlab_mod("shift-c")
step: key(f10)
step in: key(f11)
step out: key(shift-f11)
run to cursor: user.matlab_mod("alt-c")

smart indent:
    user.matlab_mod("shift-0")
    user.matlab_mod("a")
    user.matlab_mod("i")

open variable [<user.text>]:
    user.matlab_mod("0")
    insert("openvar('')")
    key(left:2)
    insert(text or "")

open file:
    user.matlab_mod("o")
    insert(text or "")

next: key(alt-down)
previous: key(alt-up)

next section: user.matlab_mod("down")
previous section: user.matlab_mod("up")
