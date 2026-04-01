app: obsidian
-
# Navigation and command-palette driven view changes.

pop daily note:
    key(cmd-p)
    insert('today daily note')
    key(enter)

pop [<user.text>] [{user.file_extension}]:
    key(cmd-o)
    edit.delete_line()
    sleep(100ms)
    insert(text or "")
    insert(file_extension or "")
    sleep(300ms)

please [<user.text>]:
    key(cmd-p)
    edit.delete_line()
    insert(text or "")

search vault | find notes:
    key(cmd-shift-f)

toggle left sidebar:
    key(cmd-p)
    edit.delete_line()
    insert("toggle left")
    key(enter)

toggle right sidebar:
    key(cmd-p)
    edit.delete_line()
    insert("toggle right")
    key(enter)

show outline:
    key(cmd-p)
    edit.delete_line()
    insert("outline")
    key(enter)
