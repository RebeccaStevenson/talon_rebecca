app: zotero
-

settings():
    key_hold = 100

# Adding Items
save: user.zotero_mod("shift-s")
new item: user.zotero_mod("shift-n")
new note: user.zotero_mod("shift-o")
import: user.zotero_mod("shift-i")
import clip: user.zotero_mod("shift-alt-i")

# Editing
add creator: key(shift-enter)
save extra: key(shift-enter)

# Removing Items
trash: key(delete)
force trash: key(shift-delete)
remove: key(delete)
delete keep: key(delete)
delete all: key(shift-delete)

# Citations
copy cite: user.zotero_mod("shift-a")
copy items: user.zotero_mod("shift-c")

# Navigation
focus library: user.zotero_mod("shift-l")
pan lib: user.zotero_mod("shift-l")
next pane: key(tab)
prev pane: key(shift-tab)
cycle tab next: user.zotero_mod("tab")
cycle tab previous: user.zotero_mod("shift-tab")
quick search: user.zotero_mod("shift-k")
find: user.zotero_mod("f")

focus contents | pan switch:
    key(tab)
    sleep(1ms)
    key(tab)
    sleep(1ms)
    key(tab)
    sleep(1ms)
    key(tab)
    sleep(1ms)
    key(tab)
    sleep(1ms)
    key(tab)
    sleep(1ms)
    key(tab)

# Tabs
next tab: user.zotero_mod("pagedown")
prev tab: user.zotero_mod("pageup")
go tab <number>: user.zotero_mod("{number}")
tab close: user.zotero_mod("w")

# Searching
find cols: user.zotero_mod(":down")

# Tags
toggle tags: user.zotero_mod("shift-t")
tag <number>: key("{number}")

# Feeds
mark all: user.zotero_mod("shift-r")
mark feed: user.zotero_mod("shift-`")

# Other
expand: key(+)
collapse: key(-)
count: user.zotero_mod("a")
rename col: key(f2)

# PDF
annotate <number>: key("alt-{number}")
pdf back: key(alt-left)
pdf next: key(alt-right)

# Notes
bold: user.zotero_mod("b")
italic: user.zotero_mod("i")
underline: user.zotero_mod("u")
select all: user.zotero_mod("a")
undo: user.zotero_mod("z")
redo: user.zotero_mod("y")
cut: user.zotero_mod("x")
copy: user.zotero_mod("c")
paste: user.zotero_mod("v")
paste plain: user.zotero_mod("shift-v")
head <number>: key("shift-alt-{number}")
format para: key(shift-alt-7)
format div: key(shift-alt-8)
format addr: key(shift-alt-9)
find replace: user.zotero_mod("f")
insert link: user.zotero_mod("k")
focus bar: key(alt-f10)
