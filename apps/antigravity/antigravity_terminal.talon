# Antigravity terminal commands.
app: antigravity
-

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
term select: user.antigravity("workbench.action.terminal.selectAll")
term clear: user.antigravity("workbench.action.terminal.clear")
term max: user.antigravity("workbench.action.toggleMaximizedPanel")
