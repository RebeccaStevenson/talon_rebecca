# Antigravity voice commands (VS Code fork)
# This file mirrors the VS Code commands for Antigravity
app: antigravity
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.multiple_cursors
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

window reload: user.antigravity("workbench.action.reloadWindow")
window close: user.antigravity("workbench.action.closeWindow")

please [<user.text>]:
    user.antigravity("workbench.action.showCommands")
    insert(user.text or "")

# Sidebar
bar explore: user.antigravity("workbench.view.explorer")
bar extensions: user.antigravity("workbench.view.extensions")
bar outline: user.antigravity("outline.focus")
bar run: user.antigravity("workbench.view.debug")
bar search: user.antigravity("workbench.view.search")
bar source: user.antigravity("workbench.view.scm")
bar test: user.antigravity("workbench.view.testing.focus")
bar switch: user.antigravity("workbench.action.toggleSidebarVisibility")
bar results: user.antigravity("search.action.focusSearchList")

# Symbol search
symbol hunt [<user.text>]:
    user.antigravity("workbench.action.gotoSymbol")
    sleep(50ms)
    insert(text or "")

symbol hunt all [<user.text>]:
    user.antigravity("workbench.action.showAllSymbols")
    sleep(50ms)
    insert(text or "")

# Panels
panel control: user.antigravity("workbench.panel.repl.view.focus")
panel output: user.antigravity("workbench.panel.output.focus")
panel problems: user.antigravity("workbench.panel.markers.view.focus")
panel switch: user.antigravity("workbench.action.togglePanel")
(pan | term) switch: user.antigravity("workbench.action.togglePanel")
(panel terminal | term): user.antigravity("workbench.action.terminal.focus")
(focus editor | ed): user.antigravity("workbench.action.focusActiveEditorGroup")

# Settings
show settings: user.antigravity("workbench.action.openGlobalSettings")
show settings json: user.antigravity("workbench.action.openSettingsJson")
show settings folder: user.antigravity("workbench.action.openFolderSettings")
show settings folder json: user.antigravity("workbench.action.openFolderSettingsFile")
show settings workspace: user.antigravity("workbench.action.openWorkspaceSettings")
show settings workspace json: user.antigravity("workbench.action.openWorkspaceSettingsFile")
show shortcuts: user.antigravity("workbench.action.openGlobalKeybindings")
show shortcuts json: user.antigravity("workbench.action.openGlobalKeybindingsFile")
show snippets: user.antigravity("workbench.action.openSnippets")

# Display
centered switch: user.antigravity("workbench.action.toggleCenteredLayout")
fullscreen switch: user.antigravity("workbench.action.toggleFullScreen")
theme switch: user.antigravity("workbench.action.selectTheme")
wrap switch: user.antigravity("editor.action.toggleWordWrap")
zen switch: user.antigravity("workbench.action.toggleZenMode")

# File Commands
file hunt [<user.text>]:
    user.antigravity("workbench.action.quickOpen")
    sleep(50ms)
    insert(text or "")
file hunt (pace | paste):
    user.antigravity("workbench.action.quickOpen")
    sleep(50ms)
    edit.paste()
file copy name: user.antigravity("fileutils.copyFileName")
file copy path: user.antigravity("copyFilePath")
file copy local [path]: user.antigravity("copyRelativeFilePath")
file create sibling: user.antigravity_and_wait("explorer.newFile")
file create: user.antigravity("workbench.action.files.newUntitledFile")
file create relative: user.antigravity("fileutils.newFile")
file create root: user.antigravity("fileutils.newFileAtRoot")
file rename:
    user.antigravity("fileutils.renameFile")
    sleep(150ms)
file move:
    user.antigravity("fileutils.moveFile")
    sleep(150ms)
file clone:
    user.antigravity("fileutils.duplicateFile")
    sleep(150ms)
file delete:
    user.antigravity("fileutils.removeFile")
    sleep(150ms)
file open folder: user.antigravity("revealFileInOS")
file reveal: user.antigravity("workbench.files.action.showActiveFileInExplorer")
save ugly: user.antigravity("workbench.action.files.saveWithoutFormatting")

# Language Features
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

# Code navigation
(go declaration | follow): user.antigravity("editor.action.revealDefinition")
go back: user.antigravity("workbench.action.navigateBack")
go forward: user.antigravity("workbench.action.navigateForward")
go implementation: user.antigravity("editor.action.goToImplementation")
go type: user.antigravity("editor.action.goToTypeDefinition")
go usage: user.antigravity("references-view.find")
go recent [<user.text>]:
    user.antigravity("workbench.action.openRecent")
    sleep(50ms)
    insert(text or "")
    sleep(250ms)
go edit: user.antigravity("workbench.action.navigateToLastEditLocation")

# Bookmarks (requires Bookmarks plugin)
bar marks: user.antigravity("workbench.view.extension.bookmarks")
toggle mark: user.antigravity("bookmarks.toggle")
go next mark: user.antigravity("bookmarks.jumpToNext")
go last mark: user.antigravity("bookmarks.jumpToPrevious")

close other tabs: user.antigravity("workbench.action.closeOtherEditors")
close all tabs: user.antigravity("workbench.action.closeAllEditors")
close tabs way right: user.antigravity("workbench.action.closeEditorsToTheRight")
close tabs way left: user.antigravity("workbench.action.closeEditorsToTheLeft")

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

# Git / Github
git branch: user.antigravity("git.branchFrom")
git branch this: user.antigravity("git.branch")
git checkout [<user.text>]:
    user.antigravity("git.checkout")
    sleep(50ms)
    insert(text or "")
git commit [<user.text>]:
    user.antigravity("git.commitStaged")
    sleep(100ms)
    user.insert_formatted(text or "", "CAPITALIZE_FIRST_WORD")
git commit undo: user.antigravity("git.undoCommit")
git commit amend: user.antigravity("git.commitStagedAmend")
git diff: user.antigravity("git.openChange")
git fetch: user.antigravity("git.fetch")
git fetch all: user.antigravity("git.fetchAll")
git ignore: user.antigravity("git.ignore")
git merge: user.antigravity("git.merge")
git output: user.antigravity("git.showOutput")
git pull: user.antigravity("git.pullRebase")
git push: user.antigravity("git.push")
git push focus: user.antigravity("git.pushForce")
git rebase abort: user.antigravity("git.rebaseAbort")
git reveal: user.antigravity("git.revealInExplorer")
git revert: user.antigravity("git.revertChange")
git stash: user.antigravity("git.stash")
git stash pop: user.antigravity("git.stashPop")
git status: user.antigravity("workbench.scm.focus")
git stage: user.antigravity("git.stage")
git stage all: user.antigravity("git.stageAll")
git sync: user.antigravity("git.sync")
git unstage: user.antigravity("git.unstage")
git unstage all: user.antigravity("git.unstageAll")
pull request: user.antigravity("pr.create")
change next: key(alt-f5)
change last: key(shift-alt-f5)

# Testing
test run: user.antigravity("testing.runAtCursor")
test run file: user.antigravity("testing.runCurrentFile")
test run all: user.antigravity("testing.runAll")
test run failed: user.antigravity("testing.reRunFailTests")
test run last: user.antigravity("testing.reRunLastRun")

test debug: user.antigravity("testing.debugAtCursor")
test debug file: user.antigravity("testing.debugCurrentFile")
test debug all: user.antigravity("testing.debugAll")
test debug failed: user.antigravity("testing.debugFailTests")
test debug last: user.antigravity("testing.debugLastRun")

test cancel: user.antigravity("testing.cancelRun")

# Debugging
break point: user.antigravity("editor.debug.action.toggleBreakpoint")
step over: user.antigravity("workbench.action.debug.stepOver")
debug step into: user.antigravity("workbench.action.debug.stepInto")
debug step out [of]: user.antigravity("workbench.action.debug.stepOut")
debug start: user.antigravity("workbench.action.debug.start")
debug pause: user.antigravity("workbench.action.debug.pause")
debug stopper: user.antigravity("workbench.action.debug.stop")
debug continue: user.antigravity("workbench.action.debug.continue")
debug restart: user.antigravity("workbench.action.debug.restart")
debug console: user.antigravity("workbench.action.debug.toggleRepl")
debug clean: user.antigravity("workbench.debug.panel.action.clearReplAction")

# Terminal
terminal external: user.antigravity("workbench.action.terminal.openNativeConsole")
term new: user.antigravity("workbench.action.terminal.new")
term next: user.antigravity("workbench.action.terminal.focusNext")
term last: user.antigravity("workbench.action.terminal.focusPrevious")
term split: user.antigravity("workbench.action.terminal.split")
term zoom: user.antigravity("workbench.action.toggleMaximizedPanel")
term trash: user.antigravity("workbench.action.terminal.kill")
term toggle: user.antigravity_and_wait("workbench.action.terminal.toggleTerminal")
term upper: user.antigravity("workbench.action.terminal.scrollUp")
term downer: user.antigravity("workbench.action.terminal.scrollDown")
term <number_small>: user.antigravity_terminal(number_small)

# Line operations
copy line down: user.antigravity("editor.action.copyLinesDownAction")
copy line up: user.antigravity("editor.action.copyLinesUpAction")

select less: user.antigravity("editor.action.smartSelect.shrink")
select (more | this): user.antigravity("editor.action.smartSelect.expand")

minimap: user.antigravity("editor.action.toggleMinimap")
maximize: user.antigravity("workbench.action.minimizeOtherEditors")
restore: user.antigravity("workbench.action.evenEditorWidths")

# Breadcrumb
select breadcrumb: user.antigravity("breadcrumbs.focusAndSelect")

replace here:
    user.replace("")
    key(cmd-alt-l)

hover show: user.antigravity("editor.action.showHover")

join lines: user.antigravity("editor.action.joinLines")

full screen: user.antigravity("workbench.action.toggleFullScreen")

curse undo: user.antigravity("cursorUndo")

select word: user.antigravity("editor.action.addSelectionToNextFindMatch")
skip word: user.antigravity("editor.action.moveSelectionToNextFindMatch")

install local: user.antigravity("workbench.extensions.action.installVSIX")
preview markdown: user.antigravity("markdown.showPreview")

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

term select: user.antigravity("workbench.action.terminal.selectAll")
term clear: user.antigravity("workbench.action.terminal.clear")
term max: user.antigravity("workbench.action.toggleMaximizedPanel")

disk: user.antigravity("workbench.action.files.save")

sidebar: user.antigravity("workbench.action.toggleSidebarVisibility")

code markdown preview: user.antigravity("markdown.showPreview")
code run notebook cell: user.antigravity("notebook.cell.execute")

# Quarto extension shortcuts
assist focus: user.antigravity("quarto-assist.focus")
assist pin: user.antigravity("quarto.assist.pin")
assist unpin: user.antigravity("quarto.assist.unpin")
clear cache: user.antigravity("quarto.clearCache")
code view assist: user.antigravity("quarto.codeViewAssist")
create project: user.antigravity("quarto.createProject")
edit source mode: user.antigravity("quarto.editInSourceMode")
edit visual mode: user.antigravity("quarto.editInVisualMode")
file create project: user.antigravity("quarto.fileCreateProject")
file new document: user.antigravity("quarto.fileNewDocument")
cell format: user.antigravity("quarto.formatCell")
cell next: user.antigravity("quarto.goToNextCell")
cell previous: user.antigravity("quarto.goToPreviousCell")
cell insert: user.antigravity("quarto.insertCodeCell")
new document: user.antigravity("quarto.newDocument")
new notebook: user.antigravity("quarto.newNotebook")
new presentation: user.antigravity("quarto.newPresentation")
preview: user.antigravity("quarto.preview")
preview content: user.antigravity("quarto.previewContentShortcut")
preview diagram: user.antigravity("quarto.previewDiagram")
preview format: user.antigravity("quarto.previewFormat")
preview math: user.antigravity("quarto.previewMath")
preview script: user.antigravity("quarto.previewScript")
document render: user.antigravity("quarto.renderDocument")
project render: user.antigravity("quarto.renderProject")
cell run all: user.antigravity("quarto.runAllCells")
cell run above: user.antigravity("quarto.runCellsAbove")
cell run below: user.antigravity("quarto.runCellsBelow")
run current: user.antigravity("quarto.runCurrent")
cell run advance: user.antigravity("quarto.runCurrentAdvance")
cell run: user.antigravity("quarto.runCurrentCell")
cell run next: user.antigravity("quarto.runNextCell")
cell run previous: user.antigravity("quarto.runPreviousCell")
run selection: user.antigravity("quarto.runSelection")
show assist: user.antigravity("quarto.showAssist")
toggle bold: user.antigravity("quarto.toggleBold")
toggle code: user.antigravity("quarto.toggleCode")
toggle italic: user.antigravity("quarto.toggleItalic")
verify installation: user.antigravity("quarto.verifyInstallation")
walkthrough new document: user.antigravity("quarto.walkthrough.newDocument")
walkthrough preview: user.antigravity("quarto.walkthrough.preview")
zotero configure library: user.antigravity("quarto.zoteroConfigureLibrary")
zotero sync web library: user.antigravity("quarto.zoteroSyncWebLibrary")
zotero unauthorized: user.antigravity("quarto.zoteroUnauthorized")


