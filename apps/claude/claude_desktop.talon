os: mac
and app.name: Claude
and app.bundle: com.anthropic.claudefordesktop
-
# Shortcuts verified from the Claude desktop app bundle on 2026-03-15.

(claude conversation new | claude new conversation): key(cmd-n)
(claude settings open | claude open settings): key(cmd-,)
(claude find | claude page find): key(cmd-f)
(claude reload | claude page reload): key(cmd-r)
(claude back | claude navigation back): key(cmd-[)
(claude forward | claude navigation forward): key(cmd-])

claude zoom in: key(cmd-=)
claude zoom out: key(cmd--)
(claude actual size | claude zoom actual): key(cmd-0)

# Menu-driven navigation for items without keyboard shortcuts.

claude about open: user.claude_desktop_menu("Claude|About Claude")
claude window show: user.claude_desktop_menu("Window|Show Main Window")
claude help open: user.claude_desktop_menu("Help|Claude Help")
claude support open: user.claude_desktop_menu("Help|Get Support")
claude logs show: user.claude_desktop_menu("Help|Troubleshooting|Show Logs in Finder")
claude installation ID copy: user.claude_desktop_menu("Help|Troubleshooting|Copy Installation ID")
claude MCP log open: user.claude_desktop_menu("Developer|Open MCP Log File")
claude MCP reload: user.claude_desktop_menu("Developer|Reload MCP Configuration")
