os: mac
app: Google Chrome
-

go to folder: key(shift-cmd-g)

preview read start: key(cmd-shift-8)
preview read premium:
    user.preview_sync_server_start()
    sleep(200ms)
    key(cmd-shift-7)
preview read stop: key(cmd-shift-9)
preview read capture:
    user.preview_sync_server_start()
    sleep(200ms)
    key(cmd-shift-u)

preview server start: user.preview_sync_server_start()
preview server stop: user.preview_sync_server_stop()
preview server restart: user.preview_sync_server_restart()
