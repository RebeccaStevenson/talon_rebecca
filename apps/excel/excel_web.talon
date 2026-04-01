app: chrome
browser.host: excel.cloud.microsoft
# title: /(Excel for the Web|Microsoft 365| Excel)/
-
tag(): user.find_and_replace

go <user.letter> <user.number_string>:
    user.excel_web_goto_cell_reference(letter + number_string)

paste special: user.excel_web_mod("alt-v")

formula: key(shift-f3)
edit: key(f2)
complete: key(alt-down)
ditto: user.excel_web_mod("'")

bold: user.excel_web_mod("b")
italic: user.excel_web_mod("i")
underline: user.excel_web_mod("u")

cell note: key(shift-f2)
cell comment: user.excel_web_mod("shift-f2")
cell menu: key(shift-f10)

column hide: user.excel_web_mod("0")
column select: user.excel_web_mod("space")

row hide: user.excel_web_mod("9")
row select: key(shift-space)

sheet new: key(shift-f11)
sheet previous: user.excel_web_mod("alt-pageup")
sheet next: user.excel_web_mod("alt-pagedown")
