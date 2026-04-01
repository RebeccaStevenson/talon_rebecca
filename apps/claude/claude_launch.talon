# Global Claude CLI launcher commands.
-
(claude start | claude launch | start claude):
    user.launch_claude_cli()

(claude start | claude launch | start claude) <user.system_path>:
    user.launch_claude_cli(system_path)

claude with prompt: insert("claude \"")

claude yolo here:
    user.launch_claude_cli("", "--dangerously-skip-permissions")

claude yolo:
    user.launch_claude_cli("", "--dangerously-skip-permissions")

claude yolo <user.system_path>:
    user.launch_claude_cli(system_path, "--dangerously-skip-permissions")

claude allow here:
    user.launch_claude_cli("", "--allow-dangerously-skip-permissions")

claude allow:
    user.launch_claude_cli("", "--allow-dangerously-skip-permissions")

claude allow <user.system_path>:
    user.launch_claude_cli(system_path, "--allow-dangerously-skip-permissions")
