app: google_sheets
-
# To enable Rango in Sheet's PWA:
tag(): browser
settings():
    key_hold = 32

# Menus

menu accessibility: key(alt-shift-a)
menu edit: key(alt-shift-e)
menu file: key(alt-shift-f)
menu format: key(alt-shift-o)
menu context: user.chrome_mod("shift-x")
menu extensions: key(alt-shift-n)
menu data: key(alt-shift-d)
menu help: key(alt-shift-h)
menu insert: key(alt-shift-i)
menu tools: key(alt-shift-t)
menu menu: key(alt-shit-v)
(menu sheet) | (sheet menu): key(alt-shift-s)

quick access: key(alt-.)

# Navigation + Selection

cell (center | focus): user.chrome_mod("backspace")
[go] row <user.number_string>: user.select_row(number_string)
[go] (col | column) <user.letters>: user.select_column(letters)
# Ex: `cell air two` selects A2
[go] cell <user.cell>: user.select_cell(cell)
# Ex: `cell air two past bat fourteen` selects A2:B14
[go] cell <user.cell_range>: user.select_cell_range(cell_range)
# Ex: If A2:B14 is selected, `past bat thirty-two` selects A2:B32
[go] past <user.cell>: user.reselect_cell_range(cell)
cell all: user.chrome_mod("a")
row (all | select): key(shift-space)
(col | column) (all | select): user.chrome_mod("space")

# Editing

spelling: key(f7)
find: user.chrome_mod("f")
replace: user.chrome_mod("h")
cell (add | insert): user.chrome_mod("alt-shift-=")

# Sheets

sheet hunt: key(shift-alt-k)
sheet new: key(shift-f11)
sheet next: user.chrome_mod("alt-]")
sheet last: user.chrome_mod("alt-[")

# Misc

please [<user.prose>]:
    key(alt-/)
    insert(prose or "")
