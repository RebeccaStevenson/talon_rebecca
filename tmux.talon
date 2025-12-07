app: iTerm
app: Terminal
-
# --- Session management ---
new session:
    user.tmux_send("c")

list sessions:
    user.tmux_send("s")

detach:
    user.tmux_send("d")

rename session:
    user.tmux_send(",")

kill session:
    user.tmux_send("&")

switch session:
    user.tmux_send("s")

# --- Window management ---
new window:
    user.tmux_send("c")

next window:
    user.tmux_send("n")

previous window:
    user.tmux_send("p")

rename window:
    user.tmux_send(",")

list windows:
    user.tmux_send("w")

kill window:
    user.tmux_send("&")

swap window left:
    user.tmux_send("{")

swap window right:
    user.tmux_send("}")

# --- Pane management ---
split vertically:
    user.tmux_send("%")

split horizontally:
    user.tmux_send('"')

close pane:
    user.tmux_send("x")

select pane left:
    user.tmux_send("h")

select pane right:
    user.tmux_send("l")

select pane up:
    user.tmux_send("k")

select pane down:
    user.tmux_send("j")

toggle pane zoom:
    user.tmux_send("z")

swap panes:
    user.tmux_send("o")

rotate panes:
    user.tmux_send("ctrl-o")

# --- Resize panes ---
resize pane left:
    user.tmux_send(":resize-pane -L", via_command=True)

resize pane right:
    user.tmux_send(":resize-pane -R", via_command=True)

resize pane up:
    user.tmux_send(":resize-pane -U", via_command=True)

resize pane down:
    user.tmux_send(":resize-pane -D", via_command=True)

# --- Copy mode and scroll ---
copy mode:
    user.tmux_send("[")

paste buffer:
    user.tmux_send("]")

# --- Miscellaneous ---
display time:
    user.tmux_send("t")

show key bindings:
    user.tmux_send("?")

lock session:
    user.tmux_send("L")

suspend tmux:
    user.tmux_send("ctrl-z")

# --- Split navigation (pane management) ---
# These commands use the 'splits' tag from tags/splits/splits.talon
go split <user.arrow_key>:
    user.tmux_keybind(arrow_key)

# Say just “go split” to temporarily display pane numbers
go split:
    user.tmux_execute_command("display-panes -d 0")
