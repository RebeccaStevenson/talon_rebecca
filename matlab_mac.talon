os: mac
and app.name: MATLAB R2013b
os: mac
and app.exe: MATLAB_maca64
os: mac
and app.name: MATLAB R2024b
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.tabs

# Navigation, searching
search: key(cmd-f)
netch | next match: key(f3)
search in files: key(cmd-shift-f)
go line: key(cmd-g)

go <number>:
    key(cmd-shift-0)
    key(cmd-g)
    insert("{number}")
    key(enter)

recenter:
    key(cmd-k)
    key(cmd-c)

[book] mark set: key(cmd-f2)
[book] mark next: key(shift-f2)

# Folding
fold: key(cmd-shift-[)
fold all:
    key(cmd-k)
    key(cmd-1)

unfold: key(cmd-shift-])
unfold all:
    key(cmd-k)
    key(cmd-j)

# Indentation
decrease indent: key(cmd-[)
increase indent: key(cmd-])
reindent: key(ctrpl-i)
no indent: key(cptrl-[:7)

end:
    insert("end")
    key(backspace)

# Miscellaneous editing
comment out: key(cmd-r)
uncomment: key(cmd-t)
scoot up: key(cmd-shift-up)
scoot down: key(cmd-shift-down)
ex kets: key(cmd-shift-m)
ex line: key(cmd-l)
ex cope: key(cmd-shift-space)

assign: insert(" = ")
eval: key(f9)
evaluate: key(f9)

# Basic
command: key(cmd-0)
editor: key(cmd-shift-0)
workspace: key(cmd-3)

run:
    key(cmd-shift-0)
    key(f5)
stop script:
    key(cmd-0)
    key(cmd-c)


# Debugging
debug start:
    key(cmd-0)
    insert("dbstop if error")
    key(enter)

debug clear:
    key(cmd-0)
    insert("dbclear all")
    key(enter)

debug stopper: key(shift-f5)
breakpoint: key(f12)
disable breakpoint: key(cmd-shift-b)
clear breakpoints: key(cmd-shift-c)
step: key(f10)
step in: key(f11)
step out: key(shift-f11)
run to cursor: key(cmd-alt-c)

smart indent:
    key(cmd-shift-0)
    key(cmd-a)
    key(cmd-i)

open variable [<user.text>]:
    key(cmd-0)
    insert("openvar('')")
    key(left:2)
    insert(text or "")
    
open file:
    key(cmd-o)
    insert(text or "")

next:
   key(alt-down)


previous:
    key(alt-up)

next section:
    key(cmd-down)
next section:
    key(cmd-up)
    






