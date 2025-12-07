#custom vscode commands go here
app: vscode
os: mac
-

# rename doesn't work with matlab, change to shortcut for now
# rename that: user.vscode("editor.action.rename")
# rename that: key(ctrl-shift-l)


# run script: key(ctr-shift-alt-r)

term copy: 
    user.vscode("workbench.action.terminal.selectAll")
    key(cmd-c)


mat run: 
    user.vscode("workbench.action.files.save")
    key(f5)
    
# repository open: key(ctrl-r)


source edit: key(shift-cmd-f4)