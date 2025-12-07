os: mac
app: excel
app: Microsoft Excel
-
# tag(): user.find_and_replace

zoom in: key("cmd-alt-=")
zoom out: key("cmd-alt--")

go <user.letter> <user.number_string>:
    key(ctrl-g)
    sleep(25ms)
    key(tab)
    insert(letter + number_string)
    key("enter")

password: key(alt-f i p e)

fill down: key(cmd-d)
fill right: key(cmd-r)
insert that: key(cmd-shift-=)
delete that: key(cmd--)

paste special: key(cmd-alt-v)

align left: key(alt-h a l)
align center: key(alt-h a c)

# filter: key(cmd-shift-f)
# sort: key(cmd-shift-r)
table: key(cmd-t)

formula: key(shift-f3)
# reference: key(cmd-t)

edit: key(f2)
complete: key(alt-down)
ditto: key(cmd-shift-')
bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)

cell note: key(shift-f2)
cell comment: key(cmd-shift-f2)
cell name: key(alt-f3)
cell menu: key(shift-f10)

column hide: key(cmd-0)
column select: key(cmd-space)
column insert: key(cmd-space cmd-shift-=)
column delete: key(cmd-space cmd--)
column top: key(cmd-up)
column bottom: key(cmd-down)
column fit: key(alt-h o i)
column filter: key(cmd-down cmd-up alt-down)
column width: key(alt-h o w)

row hide: key(cmd-9)
# row unhide: key(cmd-shift-9)
row select: key(shift-space)
row insert: key(shift-space cmd-shift-=)
row delete: key(shift-space cmd--)
row start: key(cmd-left)
row end: key(cmd-right)
row fit: key(alt-h o a)
row height: key(alt-h o h)

table select: key(cmd-a)
select all: key(cmd-a:3)

sheet new: key(shift-f11)
sheet previous: key(cmd-pageup)
sheet next: key(cmd-pagedown)
sheet rename: key(alt-h o r)

pivot that: key(alt-n v t)
# mail this: user.menu_select("File|Share|Send Workbook")

ribbon: key(cmd-f1)

window (new | open): key(alt-w n)
