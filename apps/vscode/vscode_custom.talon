# Custom VSCode commands
app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

# Custom Split/Group/Panel Management
split close others: user.vscode("workbench.action.closeEditorsInOtherGroups")
focus next group: user.vscode("workbench.action.focusNextGroup")
focus previous group: user.vscode("workbench.action.focusPreviousGroup")
# focus group <number>: user.vscode("workbench.action.focusFirstEditorGroup") # Example, needs number list
move editor next group: user.vscode("workbench.action.moveEditorToNextGroup")
move editor previous group: user.vscode("workbench.action.moveEditorToPreviousGroup")
move editor new window: user.vscode("workbench.action.moveEditorToNewWindow")
split editor: user.vscode("workbench.action.splitEditor")
split editor vertical: user.vscode("workbench.action.splitEditorDown")
split editor horizontal: user.vscode("workbench.action.splitEditorRight")
split editor orthogonal: user.vscode("workbench.action.splitEditorOrthogonal")
toggle split layout: user.vscode("workbench.action.toggleEditorGroupLayout")
close group: user.vscode("workbench.action.closeGroup")
join group: user.vscode("workbench.action.joinEditorInGroup") 
pan switch: user.vscode("workbench.action.togglePanel")
term switch: user.vscode("workbench.action.togglePanel")
term: user.vscode("workbench.action.terminal.focus")
ed: user.vscode("workbench.action.focusActiveEditorGroup")
term new: user.vscode("workbench.action.terminal.new")
term next: user.vscode("workbench.action.terminal.focusNext")
term last: user.vscode("workbench.action.terminal.focusPrevious")
term split: user.vscode("workbench.action.terminal.split")
term zoom: user.vscode("workbench.action.toggleMaximizedPanel")
term trash: user.vscode("workbench.action.terminal.kill")
term toggle: user.vscode_and_wait("workbench.action.terminal.toggleTerminal")
term upper: user.vscode("workbench.action.terminal.scrollUp")
term downer: user.vscode("workbench.action.terminal.scrollDown")
term <number_small>: user.vscode_terminal(number_small)

# MATLAB batch command template
mat batch:
    insert("matlab -batch 'run('')'")
    key(left left)

quarto preview:
    user.vscode("quarto.preview")
