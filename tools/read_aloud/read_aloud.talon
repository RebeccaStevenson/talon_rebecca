os: mac
-
read selected:
    user.read_text_aloud(edit.selected_text())

read selected system:
    user.read_text_aloud_system(edit.selected_text())

clipboard read system:
    user.read_clipboard_text_aloud_system()

(read selected tracked | tracked read selected):
    key(alt-esc)

(stop tracked reading | tracked read stop):
    key(alt-esc)

(read aloud stop | speech stop reading | system read stop):
    user.stop_read_aloud()
