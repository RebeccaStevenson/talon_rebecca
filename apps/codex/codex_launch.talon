# Global Codex launcher commands.
-
(codex | codex launch | start codex):
    user.launch_codex_cli()

((codex | codex launch | start codex) <user.system_path>):
    user.launch_codex_cli(system_path)

codex search:
    user.codex_search()

codex search <user.system_path>:
    user.codex_search(system_path)

codex allow here:
    user.launch_codex_cli("", "--full-auto")

codex allow:
    user.launch_codex_cli("", "--full-auto")

codex allow <user.system_path>:
    user.launch_codex_cli(system_path, "--full-auto")

codex yolo:
    user.launch_codex_cli("", "--full-auto")

codex yolo <user.system_path>:
    user.launch_codex_cli(system_path, "--full-auto")

codex yolo here:
    user.launch_codex_cli("", "--full-auto")
