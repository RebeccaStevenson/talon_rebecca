app: Zotero
os: mac
-

settings():
    key_hold = 100

# Adding Items
save: key(cmd-shift-s)
new item: key(cmd-shift-n)
new note: key(cmd-shift-o)
import: key(cmd-shift-i)
import clip: key(cmd-shift-alt-i)

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
copy cite: key(cmd-shift-a)
copy items: key(cmd-shift-c)

# Navigation
focus library: key(cmd-shift-l)
pan lib: key(cmd-shift-l)
next pane: key(tab)
prev pane: key(shift-tab)
next tab: key(cmd-tab)
prev tab: key(cmd-shift-tab)
quick search: key(cmd-shift-k)
find: key(cmd-f)

focus contents:
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
next tab: key(cmd-pagedown)
prev tab: key(cmd-pageup)
go tab <number>: key("cmd-{number}")
tab close: key(cmd-w)

# Searching
find cols: key(cmd:down)

# Tags
toggle tags: key(cmd-shift-t)
tag <number>: key("{number}")

# Feeds
mark all: key(cmd-shift-r)
mark feed: key(cmd-shift-`)

# Other
expand: key(+)
collapse: key(-)
count: key(cmd-a)
rename col: key(f2)

# PDF
annotate <number>: key("alt-{number}")
pdf back: key(alt-left)
pdf next: key(alt-right)

# Notes
bold: key(cmd-b)
italic: key(cmd-i)
underline: key(cmd-u)
select all: key(cmd-a)
undo: key(cmd-z)
redo: key(cmd-y)
cut: key(cmd-x)
copy: key(cmd-c)
paste: key(cmd-v)
paste plain: key(cmd-shift-v)
head <number>: key("shift-alt-{number}")
format para: key(shift-alt-7)
format div: key(shift-alt-8)
format addr: key(shift-alt-9)
find replace: key(cmd-f)
insert link: key(cmd-k)
focus bar: key(alt-f10)