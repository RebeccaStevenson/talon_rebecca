os: windows
and app.name: MATLAB R2019a
os: windows
and app.exe: matlab.exe
os: windows
and app.name: MATLAB R2023b
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.tabs

# Navigation, searching
search: key(ctrl-f)
netch | next match: key(f3)
search in files: key(ctrl-shift-f)
go line: key(ctrl-g)

go <number>:
    key(ctrl-shift-0)
    key(ctrl-g)
    insert("{number}")
    key(enter)

recenter:
    key(ctrl-k)
    key(ctrl-c)

[book] mark set: key(ctrl-f2)
[book] mark next: key(shift-f2)

# Folding
fold: key(ctrl-shift-[)
fold all:
    key(ctrl-k)
    key(ctrl-1)

unfold: key(ctrl-shift-])
unfold all:
    key(ctrl-k)
    key(ctrl-j)

# Indentation
decrease indent: key(ctrl-[)
increase indent: key(ctrl-])
reindent: key(ctrpl-i)
no indent: key(cptrl-[:7)

end:
    insert("end")
    key(backspace)

# Miscellaneous editing
comment out: key(ctrl-r)
uncomment: key(ctrl-t)
scoot up: key(ctrl-shift-up)
scoot down: key(ctrl-shift-down)
ex kets: key(ctrl-shift-m)
ex line: key(ctrl-l)
ex cope: key(ctrl-shift-space)

assign: insert(" = ")
eval: key(f9)
evaluate: key(f9)

# Basic
command: key(ctrl-0)
editor: key(ctrl-shift-0)
workspace: key(ctrl-3)

run:
    key(ctrl-shift-0)
    key(f5)
stop script:
    key(ctrl-0)
    key(ctrl-c)


# Debugging
debug start:
    key(ctrl-0)
    insert("dbstop if error")
    key(enter)

debug clear:
    key(ctrl-0)
    insert("dbclear all")
    key(enter)

debug stopper: key(shift-f5)
breakpoint: key(f12)
disable breakpoint: key(ctrl-shift-b)
clear breakpoints: key(ctrl-shift-c)
step: key(f10)
step in: key(f11)
step out: key(shift-f11)
run to cursor: key(ctrl-alt-c)

smart indent:
    key(ctrl-shift-0)
    key(ctrl-a)
    key(ctrl-i)

open variable [<user.text>]:
    key(ctrl-0)
    insert("openvar('')")
    key(left:2)
    insert(text or "")
    
open file:
    key(ctrl-o)
    insert(text or "")

next:
   key(alt-down)


previous:
    key(alt-up)

next section:
    key(ctrl-down)
previous section:
    key(ctrl-up)
    






