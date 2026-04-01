# Antigravity editing, refactor, comment, and folding commands.
app: antigravity
-

# Language features
suggest show: user.antigravity("editor.action.triggerSuggest")
hint show: user.antigravity("editor.action.triggerParameterHints")
definition show: user.antigravity("editor.action.revealDefinition")
definition peek: user.antigravity("editor.action.peekDefinition")
definition side: user.antigravity("editor.action.revealDefinitionAside")
references show: user.antigravity("editor.action.goToReferences")
hierarchy peek: user.antigravity("editor.showCallHierarchy")
references find: user.antigravity("references-view.find")
format that: user.antigravity("editor.action.formatDocument")
format selection: user.antigravity("editor.action.formatSelection")
imports fix: user.antigravity("editor.action.organizeImports")
problem next: user.antigravity("editor.action.marker.nextInFiles")
problem last: user.antigravity("editor.action.marker.prevInFiles")
problem fix: user.antigravity("problems.action.showQuickFixes")
refactor that: user.antigravity("editor.action.refactor")
whitespace trim: user.antigravity("editor.action.trimTrailingWhitespace")
language switch: user.antigravity("workbench.action.editor.changeLanguageMode")
refactor rename: user.antigravity("editor.action.rename")
refactor this: user.antigravity("editor.action.refactor")

# Folding
fold that: user.antigravity("editor.fold")
unfold that: user.antigravity("editor.unfold")
fold those: user.antigravity("editor.foldAllMarkerRegions")
unfold those: user.antigravity("editor.unfoldRecursively")
fold all: user.antigravity("editor.foldAll")
unfold all: user.antigravity("editor.unfoldAll")
fold comments: user.antigravity("editor.foldAllBlockComments")
fold one: user.antigravity("editor.foldLevel1")
fold two: user.antigravity("editor.foldLevel2")
fold three: user.antigravity("editor.foldLevel3")
fold four: user.antigravity("editor.foldLevel4")
fold five: user.antigravity("editor.foldLevel5")
fold six: user.antigravity("editor.foldLevel6")
fold seven: user.antigravity("editor.foldLevel7")

# Line operations and selection growth
copy line down: user.antigravity("editor.action.copyLinesDownAction")
copy line up: user.antigravity("editor.action.copyLinesUpAction")
select less: user.antigravity("editor.action.smartSelect.shrink")
select (more | this): user.antigravity("editor.action.smartSelect.expand")
select word: user.antigravity("editor.action.addSelectionToNextFindMatch")
skip word: user.antigravity("editor.action.moveSelectionToNextFindMatch")
curse undo: user.antigravity("cursorUndo")

replace here:
    user.replace("")
    key(cmd-alt-l)

hover show: user.antigravity("editor.action.showHover")
join lines: user.antigravity("editor.action.joinLines")

# Comments
todo comment:
    insert("TODO: ")

important comment:
    insert("! ")

question comment:
    insert("? ")

temporary comment:
    insert("TEMP: ")

info comment:
    insert("* ")

code run notebook cell: user.antigravity("notebook.cell.execute")
