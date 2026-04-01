# Antigravity navigation and workbench movement commands.
app: antigravity
-

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
sidebar: user.antigravity("workbench.action.toggleSidebarVisibility")

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

# Bookmarks
bar marks: user.antigravity("workbench.view.extension.bookmarks")
toggle mark: user.antigravity("bookmarks.toggle")
go next mark: user.antigravity("bookmarks.jumpToNext")
go last mark: user.antigravity("bookmarks.jumpToPrevious")

# Breadcrumb
select breadcrumb: user.antigravity("breadcrumbs.focusAndSelect")
