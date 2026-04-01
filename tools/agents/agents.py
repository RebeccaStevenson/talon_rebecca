"""Shared agent harness lists and command dispatch helpers."""

from talon import Context, Module, actions, app


mod = Module()
mod.list("agent_harness", desc="Supported AI agent harnesses")
mod.list("agent_launch_flag", desc="Shared launch flags for supported AI agent harnesses")
mod.list("agent_plain_slash_command", desc="Shared slash commands without launch-flag collisions")
mod.list("agent_slash_command", desc="Shared slash commands for supported AI agent harnesses")

ctx = Context()
ctx.lists["user.agent_harness"] = {
    "codex": "codex",
    "claude": "claude",
}
ctx.lists["user.agent_launch_flag"] = {
    "allow": "allow",
    "resume": "resume",
    "yolo": "yolo",
}
ctx.lists["user.agent_plain_slash_command"] = {
    "clear": "clear",
    "compact": "compact",
    "diff": "diff",
    "help": "help",
    "init": "init",
    "mcp": "mcp",
    "model": "model",
    "permissions": "permissions",
    "plan": "plan",
    "quit command": "quit",
}
ctx.lists["user.agent_slash_command"] = {
    **ctx.lists["user.agent_plain_slash_command"],
    "resume": "resume",
}

_SLASH_COMMANDS = {
    "clear": {
        "codex": "/clear",
        "claude": "/clear",
    },
    "compact": {
        "codex": "/compact",
        "claude": "/compact",
    },
    "diff": {
        "codex": "/diff",
        "claude": "/diff",
    },
    "help": {
        "codex": "/help",
        "claude": "/help",
    },
    "init": {
        "codex": "/init",
        "claude": "/init",
    },
    "mcp": {
        "codex": "/mcp",
        "claude": "/mcp",
    },
    "model": {
        "codex": "/model",
        "claude": "/model",
    },
    "permissions": {
        "codex": "/permissions",
        "claude": "/permissions",
    },
    "plan": {
        "codex": "/plan",
        "claude": "/plan",
    },
    "quit": {
        "codex": "/quit",
        "claude": "/exit",
    },
    "resume": {
        "codex": "/resume",
        "claude": "/resume",
    },
}

_KEY_COMMANDS = {
    "cancel": {
        "codex": "ctrl-c",
        "claude": "ctrl-c",
    },
    "interrupt": {
        "codex": "ctrl-c",
        "claude": "ctrl-c",
    },
    "quit": {
        "codex": "ctrl-c ctrl-c",
        "claude": "ctrl-d",
    },
}


def _normalized_agent(agent: str) -> str:
    normalized = agent.strip().lower()
    if normalized not in ctx.lists["user.agent_harness"].values():
        raise ValueError(f"Unsupported agent harness: {agent}")
    return normalized


def _resolve_mapping(agent: str, intent: str, mapping: dict[str, dict[str, str]]) -> str:
    normalized_agent = _normalized_agent(agent)
    normalized_intent = intent.strip().lower()
    if normalized_intent not in mapping:
        raise ValueError(f"Unsupported agent intent: {intent}")
    return mapping[normalized_intent][normalized_agent]


@mod.action_class
class Actions:
    def agent_cli_insert_slash(agent: str, intent: str) -> None:
        """Insert an agent-specific slash command for a shared intent."""
        try:
            actions.insert(_resolve_mapping(agent, intent, _SLASH_COMMANDS))
        except ValueError as error:
            app.notify("Agent command unavailable", str(error))

    def agent_cli_key(agent: str, intent: str) -> None:
        """Press the keybinding for a shared agent CLI intent."""
        try:
            actions.key(_resolve_mapping(agent, intent, _KEY_COMMANDS))
        except ValueError as error:
            app.notify("Agent command unavailable", str(error))
