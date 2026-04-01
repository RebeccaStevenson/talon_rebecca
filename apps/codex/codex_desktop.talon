os: mac
and app.name: Codex
and app.bundle: com.openai.codex
-
# Shortcuts verified from the Codex desktop app bundle on 2026-03-15.
# Palette commands below are driven by visible command menu labels.

codex command menu: key(cmd-shift-p)
codex command menu alt: key(cmd-k)
codex keyboard shortcuts: key(cmd-/)
codex shortcuts open: key(cmd-/)
codex settings open: key(cmd-,)

codex reload skills:
    key(cmd-shift-p)
    sleep(150ms)
    insert("Force reload skills")
    sleep(100ms)
    key(enter)

codex go to skills:
    key(cmd-shift-p)
    sleep(150ms)
    insert("Go to skills")
    sleep(100ms)
    key(enter)

codex MCP:
    key(cmd-shift-p)
    sleep(150ms)
    insert("MCP")
    sleep(100ms)
    key(enter)

codex personality:
    key(cmd-shift-p)
    sleep(150ms)
    insert("Personality")
    sleep(100ms)
    key(enter)

codex thread new: key(cmd-n)
codex thread new alt: key(cmd-shift-o)
(codex find | codex thread find): key(cmd-f)
(codex previous thread | codex thread previous): key(cmd-shift-[)
(codex next thread | codex thread next): key(cmd-shift-])
codex thread pin: key(cmd-alt-p)
codex thread rename: key(cmd-ctrl-r)
codex thread archive: key(cmd-shift-a)

(codex folder open | codex open folder): key(cmd-o)

(codex toggle sidebar | codex sidebar toggle): key(cmd-b)
(codex toggle terminal | codex terminal toggle): key(cmd-j)
(codex toggle diff panel | codex diff toggle): key(cmd-alt-b)
codex trace toggle: key(cmd-shift-s)

codex back: key(cmd-[)
codex forward: key(cmd-])

codex conversation path copy: key(cmd-alt-shift-c)
codex working directory copy: key(cmd-shift-c)
codex session ID copy: key(cmd-alt-c)
codex deeplink copy: key(cmd-alt-l)
