os: mac
app: Google Chrome
browser.host: excel.cloud.microsoft
# title: /(Excel for the Web|Microsoft 365| Excel)/

tag(): user.find_and_replace

zoom in: key(cmd-alt-=)
zoom out: key(cmd-alt--)

go <user.letter> <user.number_string>:
    key(cmd-g)
    sleep(50ms)
    key(cmd-a)
    key(backspace)
    insert(letter + number_string)
    key("enter")

fill down: key(cmd-d)
fill right: key(cmd-r)
insert that: key(cmd-shift-=)
delete that: key(cmd--)
paste special: key(cmd-ctrl-v)

align left: key(cmd-l)
align center: key(cmd-e)

filter: key(cmd-shift-f)
table: key(cmd-t)

formula: key(shift-f3)
edit: key(ctrl-u)
complete: key(alt-down)
ditto: key(cmd-')

bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)

cell note: key(shift-f2)
cell comment: key(cmd-shift-f2)
cell menu: key(shift-f10)

column hide: key(ctrl-0)
column select: key(ctrl-space)
column insert: key(ctrl-space cmd-shift-=)
column delete: key(ctrl-space cmd--)
column top: key(cmd-up)
column bottom: key(cmd-down)
column filter: key(alt-down)

row hide: key(ctrl-9)
row select: key(shift-space)
row insert: key(shift-space cmd-shift-=)
row delete: key(shift-space cmd--)
row start: key(cmd-left)
row end: key(cmd-right)

table select: key(cmd-a)
select all: key(cmd-a:3)

sheet new: key(shift-f11)
sheet previous: key(cmd-pageup)
sheet next: key(cmd-pagedown)
ribbon: key(cmd-alt-r)
