app: windsurf
os: mac
-

########################
# Command Chat
########################
windsurf command:                key(cmd-i)
windsurf accept command:         key(cmd-enter)
windsurf reject command:         key(cmd-backspace)

# Chat helpers
windsurf new chat:               user.vscode("windsurf.prioritized.chat.openNewConversation")
windsurf problem chat:           user.vscode("windsurf.prioritized.chat.openFromProblemsPanel")
windsurf explain:                user.vscode("windsurf.explain")
windsurf refactor:               user.vscode("windsurf.refactorFunction")
windsurf docstring:              user.vscode("windsurf.generateFunctionDocstring")
windsurf commit:                 user.vscode("windsurf.generateCommitMessage")

########################
# Cascade (multi‑file AI edits)
########################
windsurf cascade:                key(shift-cmd-i)
cascade accept all:              key(cmd-enter)
cascade reject all:              key(cmd-backspace)

cascade next hunk:               key(alt-j)
cascade previous hunk:           key(alt-k)
cascade next file:               key(alt-l)
cascade previous file:           key(alt-h)
cascade accept hunk:             key(alt-enter)
cascade reject hunk:             key(shift-alt-backspace)

# Cascade extras
windsurf auto-cascade:           user.vscode("windsurf.triggerAutoCascade")
open diff zones:                 user.vscode("windsurf.openDiffZones")
close diff zones:                user.vscode("windsurf.closeAllDiffZones")
focus cascade panel:             user.vscode("windsurf.cascadePanel.focus")

########################
# Inline suggestions & autocomplete
########################
windsurf complete:               key(tab)
windsurf cancel complete:        key(escape)
windsurf suggest:                key(alt-\\)
snooze autocomplete:             user.vscode("windsurf.snoozeAutocomplete")

# synonym for windsurf complete
accept line:
    key(tab)


# synonym for windsurf cancel complete
dismiss line:
    key(escape)


########################
# Terminal helpers
########################
windsurf run terminal command:   key(cmd-enter)
terminal accept suggestion:      key(alt-enter)
terminal reject suggestion:      key(cmd-backspace)
windsurf chat here:              user.vscode("windsurf.chatFromTerminal")
run terminal suggestion:         key(alt-enter)

########################
# Settings & documentation
########################
windsurf quick settings:         user.vscode("windsurf.openQuickSettingsPanel")
windsurf docs:                   user.vscode("windsurf.openDocs")

########################
# Maintenance / Rescue
########################
restart language server:         user.vscode("windsurf.restartLanguageServer")
refresh winds servers:           user.vscode("windsurf.refreshMcpServers")
windsurf settings import:        user.vscode("windsurf.importVSCodeSettings")
