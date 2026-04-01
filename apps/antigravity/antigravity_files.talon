# Antigravity file, settings, display, and editor layout commands.
app: antigravity
-

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
full screen: user.antigravity("workbench.action.toggleFullScreen")
minimap: user.antigravity("editor.action.toggleMinimap")
maximize: user.antigravity("workbench.action.minimizeOtherEditors")
restore: user.antigravity("workbench.action.evenEditorWidths")

# File commands
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
disk: user.antigravity("workbench.action.files.save")

close other tabs: user.antigravity("workbench.action.closeOtherEditors")
close all tabs: user.antigravity("workbench.action.closeAllEditors")
close tabs way right: user.antigravity("workbench.action.closeEditorsToTheRight")
close tabs way left: user.antigravity("workbench.action.closeEditorsToTheLeft")

install local: user.antigravity("workbench.extensions.action.installVSIX")
preview markdown: user.antigravity("markdown.showPreview")
code markdown preview: user.antigravity("markdown.showPreview")
