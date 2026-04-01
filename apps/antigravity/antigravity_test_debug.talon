# Antigravity testing and debugging commands.
app: antigravity
-

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
