# Antigravity git and source control commands.
app: antigravity
-

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
