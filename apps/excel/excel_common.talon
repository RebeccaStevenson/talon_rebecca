app: excel
-
# tag(): user.find_and_replace

zoom in: user.excel_mod("alt-=")
zoom out: user.excel_mod("alt--")

go <user.letter> <user.number_string>:
    user.excel_desktop_goto_cell_reference(letter + number_string)

password: key(alt-f i p e)

fill down: user.excel_mod("d")
fill right: user.excel_mod("r")
insert that: user.excel_mod("shift-=")
delete that: user.excel_mod("-")

paste special: user.excel_mod("alt-v")

align left: key(alt-h a l)
align center: key(alt-h a c)

# filter: key(cmd-shift-f)
# sort: key(cmd-shift-r)
table: user.excel_mod("t")

formula: key(shift-f3)
# reference: key(cmd-t)

edit: key(f2)
complete: key(alt-down)
ditto: user.excel_mod("shift-'")
bold: user.excel_mod("b")
italic: user.excel_mod("i")
underline: user.excel_mod("u")

cell note: key(shift-f2)
cell comment: user.excel_mod("shift-f2")
cell name: key(alt-f3)
cell menu: key(shift-f10)

column hide: user.excel_mod("0")
column select: user.excel_mod("space")
column insert:
    user.excel_mod("space")
    user.excel_mod("shift-=")
column delete:
    user.excel_mod("space")
    user.excel_mod("-")
column top: user.excel_mod("up")
column bottom: user.excel_mod("down")
column fit: key(alt-h o i)
column filter:
    user.excel_mod("down")
    user.excel_mod("up")
    key(alt-down)
column width: key(alt-h o w)

row hide: user.excel_mod("9")
# row unhide: key(cmd-shift-9)
row select: key(shift-space)
row insert:
    key(shift-space)
    user.excel_mod("shift-=")
row delete:
    key(shift-space)
    user.excel_mod("-")
row start: user.excel_mod("left")
row end: user.excel_mod("right")
row fit: key(alt-h o a)
row height: key(alt-h o h)

table select: user.excel_mod("a")
select all: user.excel_mod("a:3")

sheet new: key(shift-f11)
sheet previous: user.excel_mod("pageup")
sheet next: user.excel_mod("pagedown")
sheet rename: key(alt-h o r)

pivot that: key(alt-n v t)
# mail this: user.menu_select("File|Share|Send Workbook")

ribbon: user.excel_mod("f1")

window (new | open): key(alt-w n)
