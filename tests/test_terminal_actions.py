"""Tests for terminal launch helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.system.terminal_actions as terminal_actions
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()

    def test_open_new_terminal_window_uses_existing_terminal():
        calls = []

        actions.register_test_action(
            "user", "switcher_focus", lambda name: calls.append(("focus", name))
        )
        actions.register_test_action("", "key", lambda combo: calls.append(("key", combo)))

        actions.user.open_new_terminal_window()

        assert ("focus", "terminal") in calls
        assert ("key", "cmd-n") in calls

    def test_open_new_terminal_window_launches_terminal_when_missing(monkeypatch):
        launches = []
        key_calls = []

        def _missing_terminal(_name):
            raise RuntimeError('App not running: "terminal"')

        actions.register_test_action("user", "switcher_focus", _missing_terminal)
        actions.register_test_action("", "key", lambda combo: key_calls.append(combo))
        monkeypatch.setattr(
            terminal_actions.subprocess,
            "Popen",
            lambda args: launches.append(args),
        )

        actions.user.open_new_terminal_window()

        assert launches == [["open", "-a", "Terminal"]]
        assert key_calls == []

    def test_close_terminal_window_ignores_missing_terminal():
        def _missing_terminal(_name):
            raise RuntimeError('App not running: "terminal"')

        actions.register_test_action("user", "switcher_focus", _missing_terminal)

        actions.user.close_terminal_window()

        assert app.notifications == []

    def test_run_command_in_new_terminal_uses_osascript_on_mac(monkeypatch):
        inserts = []
        keys = []
        runs = []

        actions.register_test_action("", "insert", lambda text: inserts.append(text))
        actions.register_test_action("", "key", lambda combo: keys.append(combo))

        def _fake_run(args, check=False, stdout=None, stderr=None):
            runs.append(
                {
                    "args": args,
                    "check": check,
                    "stdout": stdout,
                    "stderr": stderr,
                }
            )

            class _Result:
                returncode = 0

            return _Result()

        monkeypatch.setattr(terminal_actions.subprocess, "run", _fake_run)

        actions.user.run_command_in_new_terminal("claude", close_after=False)

        assert len(runs) == 1
        assert runs[0]["args"][0] == "osascript"
        assert 'tell application "Terminal" to activate' in runs[0]["args"]
        assert 'tell application "Terminal" to do script "claude"' in runs[0]["args"]
        assert inserts == []
        assert keys == []

    def test_run_command_in_new_terminal_appends_exit_when_closing_on_mac(monkeypatch):
        runs = []

        def _fake_run(args, check=False, stdout=None, stderr=None):
            runs.append(args)

            class _Result:
                returncode = 0

            return _Result()

        monkeypatch.setattr(terminal_actions.subprocess, "run", _fake_run)

        actions.user.run_command_in_new_terminal("pwd", close_after=True)

        assert len(runs) == 1
        assert 'tell application "Terminal" to do script "pwd\nexit"' in runs[0]

    def test_launch_codex_cli_quotes_path_and_suffix(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, press_enter=True, close_after=True, post_command_delay="300ms": calls.append(
                {
                    "command": command,
                    "press_enter": press_enter,
                    "close_after": close_after,
                    "post_command_delay": post_command_delay,
                }
            ),
        )
        monkeypatch.setattr(terminal_actions, "expand_path", lambda path: "/tmp/project folder")

        actions.user.launch_codex_cli("~/project folder", "--full-auto")

        assert calls == [
            {
                "command": "codex --cd '/tmp/project folder' --full-auto",
                "press_enter": True,
                "close_after": False,
                "post_command_delay": "1s",
            }
        ]

    def test_launch_codex_cli_uses_windows_quoting_when_platform_changes(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, press_enter=True, close_after=True, post_command_delay="300ms": calls.append(
                {
                    "command": command,
                    "press_enter": press_enter,
                    "close_after": close_after,
                    "post_command_delay": post_command_delay,
                }
            ),
        )
        monkeypatch.setattr(terminal_actions.app, "platform", "windows")
        monkeypatch.setattr(
            terminal_actions,
            "expand_path",
            lambda path: r'C:\Users\rebec\project "folder"',
        )

        actions.user.launch_codex_cli(r"~\project folder", "--search")

        assert calls == [
            {
                "command": 'codex --cd "C:\\Users\\rebec\\project `"folder`"" --search',
                "press_enter": True,
                "close_after": False,
                "post_command_delay": "1s",
            }
        ]

    def test_launch_claude_cli_changes_directory_before_launch(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, press_enter=True, close_after=True, post_command_delay="300ms": calls.append(
                {
                    "command": command,
                    "press_enter": press_enter,
                    "close_after": close_after,
                    "post_command_delay": post_command_delay,
                }
            ),
        )
        monkeypatch.setattr(
            terminal_actions,
            "command_with_directory",
            lambda command, path: f"cd '/tmp/project folder'\n{command}",
        )

        actions.user.launch_claude_cli("~/project folder", "--dangerously-skip-permissions")

        assert calls == [
            {
                "command": "cd '/tmp/project folder'\nclaude --dangerously-skip-permissions",
                "press_enter": True,
                "close_after": False,
                "post_command_delay": "1s",
            }
        ]

    def test_launch_codex_cli_changes_directory_before_resume_subcommand(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, press_enter=True, close_after=True, post_command_delay="300ms": calls.append(
                {
                    "command": command,
                    "press_enter": press_enter,
                    "close_after": close_after,
                    "post_command_delay": post_command_delay,
                }
            ),
        )
        monkeypatch.setattr(
            terminal_actions,
            "command_with_directory",
            lambda command, path: f"cd '/tmp/project folder'\n{command}",
        )

        actions.user.launch_codex_cli("~/project folder", "resume")

        assert calls == [
            {
                "command": "cd '/tmp/project folder'\ncodex resume",
                "press_enter": True,
                "close_after": False,
                "post_command_delay": "1s",
            }
        ]

    def test_launch_codex_cli_appends_prompt_in_target_directory(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, press_enter=True, close_after=True, post_command_delay="300ms": calls.append(
                {
                    "command": command,
                    "press_enter": press_enter,
                    "close_after": close_after,
                    "post_command_delay": post_command_delay,
                }
            ),
        )
        monkeypatch.setattr(terminal_actions, "expand_path", lambda path: "/tmp/project folder")

        actions.user.launch_codex_cli("~/project folder", prompt="refactor this code base")

        assert calls == [
            {
                "command": "codex --cd '/tmp/project folder' 'refactor this code base'",
                "press_enter": True,
                "close_after": False,
                "post_command_delay": "1s",
            }
        ]

    def test_launch_claude_cli_appends_prompt_in_target_directory(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "run_command_in_new_terminal",
            lambda command, press_enter=True, close_after=True, post_command_delay="300ms": calls.append(
                {
                    "command": command,
                    "press_enter": press_enter,
                    "close_after": close_after,
                    "post_command_delay": post_command_delay,
                }
            ),
        )
        monkeypatch.setattr(
            terminal_actions,
            "command_with_directory",
            lambda command, path: f"cd '/tmp/project folder'\n{command}",
        )

        actions.user.launch_claude_cli("~/project folder", prompt="refactor this code base")

        assert calls == [
            {
                "command": "cd '/tmp/project folder'\nclaude 'refactor this code base'",
                "press_enter": True,
                "close_after": False,
                "post_command_delay": "1s",
            }
        ]

    def test_agent_cli_launch_routes_codex_yolo(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_codex_cli",
            lambda path=None, command_suffix=None: calls.append((path, command_suffix)),
        )

        actions.user.agent_cli_launch("codex", "~/project folder", "yolo")

        assert calls == [
            ("~/project folder", "--dangerously-bypass-approvals-and-sandbox")
        ]

    def test_agent_cli_launch_routes_claude_default(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_claude_cli",
            lambda path=None, command_suffix=None: calls.append((path, command_suffix)),
        )

        actions.user.agent_cli_launch("claude")

        assert calls == [(None, None)]

    def test_agent_cli_launch_routes_codex_resume(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_codex_cli",
            lambda path=None, command_suffix=None: calls.append((path, command_suffix)),
        )

        actions.user.agent_cli_launch("codex", mode="resume")

        assert calls == [(None, "resume")]

    def test_agent_cli_launch_routes_codex_resume_with_path(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_codex_cli",
            lambda path=None, command_suffix=None: calls.append((path, command_suffix)),
        )

        actions.user.agent_cli_launch("codex", "~/project folder", "resume")

        assert calls == [("~/project folder", "resume")]

    def test_agent_cli_launch_with_prompt_routes_codex(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_codex_cli",
            lambda path=None, command_suffix=None, prompt=None: calls.append(
                (path, command_suffix, prompt)
            ),
        )

        actions.user.agent_cli_launch_with_prompt(
            "codex", "~/project folder", "refactor this code base"
        )

        assert calls == [("~/project folder", None, "refactor this code base")]

    def test_agent_cli_launch_with_prompt_routes_claude(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_claude_cli",
            lambda path=None, command_suffix=None, prompt=None: calls.append(
                (path, command_suffix, prompt)
            ),
        )

        actions.user.agent_cli_launch_with_prompt(
            "claude", "~/project folder", "refactor this code base"
        )

        assert calls == [("~/project folder", None, "refactor this code base")]

    def test_agent_cli_launch_with_prompt_routes_codex_yolo(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_codex_cli",
            lambda path=None, command_suffix=None, prompt=None: calls.append(
                (path, command_suffix, prompt)
            ),
        )

        actions.user.agent_cli_launch_with_prompt(
            "codex", "~/project folder", "refactor this code base", "yolo"
        )

        assert calls == [
            (
                "~/project folder",
                "--dangerously-bypass-approvals-and-sandbox",
                "refactor this code base",
            )
        ]

    def test_agent_cli_launch_with_prompt_routes_claude_resume(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_claude_cli",
            lambda path=None, command_suffix=None, prompt=None: calls.append(
                (path, command_suffix, prompt)
            ),
        )

        actions.user.agent_cli_launch_with_prompt(
            "claude", "~/project folder", "refactor this code base", "resume"
        )

        assert calls == [("~/project folder", "--resume", "refactor this code base")]

    def test_agent_cli_launch_routes_claude_resume_with_path(monkeypatch):
        calls = []

        actions.register_test_action(
            "user",
            "launch_claude_cli",
            lambda path=None, command_suffix=None: calls.append((path, command_suffix)),
        )

        actions.user.agent_cli_launch("claude", "~/project folder", "resume")

        assert calls == [("~/project folder", "--resume")]
