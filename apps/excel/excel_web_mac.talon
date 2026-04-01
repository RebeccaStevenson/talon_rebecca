os: mac
app: chrome
browser.host: excel.cloud.microsoft
# title: /(Excel for the Web|Microsoft 365| Excel)/
-
# These chords are Rebecca-specific macOS/browser overrides.
# They are intentionally kept separate from the shared Excel-for-the-web file
# because current Microsoft docs do not clearly document them as canonical
# Excel for the web shortcuts on Mac.
# Treat this file as provisional until each command is validated in-app against
# the current override-browser-shortcuts behavior.

zoom in: key(cmd-alt-=)
zoom out: key(cmd-alt--)

fill down: key(cmd-d)
fill right: key(cmd-r)
insert that: key(cmd-shift-=)
delete that: key(cmd--)

align left: key(cmd-l)
align center: key(cmd-e)

filter: key(cmd-shift-f)
table: key(cmd-t)

column insert: key(ctrl-space cmd-shift-=)
column delete: key(ctrl-space cmd--)
column top: key(cmd-up)
column bottom: key(cmd-down)
column filter: key(alt-down)

row insert: key(shift-space cmd-shift-=)
row delete: key(shift-space cmd--)
row start: key(cmd-left)
row end: key(cmd-right)

table select: key(cmd-a)
select all: key(cmd-a:3)

ribbon: key(cmd-alt-r)
