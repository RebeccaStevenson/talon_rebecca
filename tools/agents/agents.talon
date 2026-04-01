# Shared voice surface for Codex and Claude harnesses.
-

{user.agent_harness}:
    user.agent_cli_launch(agent_harness)

{user.agent_harness} <user.system_path>:
    user.agent_cli_launch(agent_harness, system_path)

{user.agent_harness} <user.system_path> <user.text>:
    user.agent_cli_launch_with_prompt(agent_harness, system_path, text)

{user.agent_harness} {user.agent_launch_flag}:
    user.agent_cli_launch(agent_harness, "", agent_launch_flag)

{user.agent_harness} {user.agent_launch_flag} <user.system_path>:
    user.agent_cli_launch(agent_harness, system_path, agent_launch_flag)

{user.agent_harness} {user.agent_launch_flag} <user.system_path> <user.text>:
    user.agent_cli_launch_with_prompt(agent_harness, system_path, text, agent_launch_flag)

{user.agent_harness} cancel:
    user.agent_cli_key(agent_harness, "cancel")

{user.agent_harness} interrupt:
    user.agent_cli_key(agent_harness, "interrupt")

{user.agent_harness} quit:
    user.agent_cli_key(agent_harness, "quit")

{user.agent_harness} {user.agent_plain_slash_command}:
    user.agent_cli_insert_slash(agent_harness, agent_plain_slash_command)

{user.agent_harness} slash {user.agent_slash_command}:
    user.agent_cli_insert_slash(agent_harness, agent_slash_command)

{user.agent_harness} allow here:
    user.agent_cli_launch(agent_harness, "", "allow")

{user.agent_harness} yolo here:
    user.agent_cli_launch(agent_harness, "", "yolo")

# Preserve the older Codex phrase while routing to the current slash command.
codex approvals:
    user.agent_cli_insert_slash("codex", "permissions")
