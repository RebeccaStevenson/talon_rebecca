app: Zotero
os: win
-

settings():
    key_hold = 100

# Adding Items
save: key(ctrl-shift-s)
new item: key(ctrl-shift-n)
new note: key(ctrl-shift-o)
import: key(ctrl-shift-i)
import clip: key(ctrl-shift-alt-i)

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
copy cite: key(ctrl-shift-a)
copy items: key(ctrl-shift-c)

# Navigation
focus library: key(ctrl-shift-l)
pan lib: key(ctrl-shift-l)
next pane: key(tab)
prev pane: key(shift-tab)
next tab: key(ctrl-tab)
prev tab: key(ctrl-shift-tab)
quick search: key(ctrl-shift-k)
find: key(ctrl-f)

pan switch:
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
next tab: key(ctrl-pagedown)
prev tab: key(ctrl-pageup)
go tab <number>: key("ctrl-{number}")
tab close: key(ctrl-w)

# Searching
find cols: key(ctrl:down)

# Tags
toggle tags: key(ctrl-shift-t)
tag <number>: key("{number}")

# Feeds
mark all: key(ctrl-shift-r)
mark feed: key(ctrl-shift-`)

# Other
expand: key(+)
collapse: key(-)
count: key(ctrl-a)
rename col: key(f2)

# PDF
annotate <number>: key("alt-{number}")
pdf back: key(alt-left)
pdf next: key(alt-right)

# Notes
bold: key(ctrl-b)
italic: key(ctrl-i)
underline: key(ctrl-u)
select all: key(ctrl-a)
undo: key(ctrl-z)
redo: key(ctrl-y)
cut: key(ctrl-x)
copy: key(ctrl-c)
paste: key(ctrl-v)
paste plain: key(ctrl-shift-v)
head <number>: key("shift-alt-{number}")
format para: key(shift-alt-7)
format div: key(shift-alt-8)
format addr: key(shift-alt-9)
find replace: key(ctrl-f)
insert link: key(ctrl-k)
focus bar: key(alt-f10)