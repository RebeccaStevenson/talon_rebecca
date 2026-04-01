os: mac
-
cursor here:
    user.switcher_focus('terminal')
    sleep(200ms)
    insert('cursor "$(osascript -e \'tell application "Finder" to get POSIX path of (target of window 1 as alias)\')"')
    key(enter)

# Windsurf launchers
windsurf edit <user.system_path>:
    user.switcher_focus('terminal')
    sleep(200ms)
    insert("windsurf " + system_path)
    key(enter)

windsurf here:
    user.switcher_focus('terminal')
    sleep(200ms)
    insert('windsurf "$(osascript -e \'tell application "Finder" to get POSIX path of (target of window 1 as alias)\')"')
    key(enter)
