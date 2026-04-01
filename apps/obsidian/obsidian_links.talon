app: obsidian
-
# Link- and note-relationship views.

show backlinks:
    key(cmd-p)
    edit.delete_line()
    insert("backlinks")
    key(enter)

show outgoing links:
    key(cmd-p)
    edit.delete_line()
    insert("outgoing links")
    key(enter)

show bookmarks:
    key(cmd-p)
    edit.delete_line()
    insert("bookmarks")
    key(enter)
