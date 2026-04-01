"""Shared helpers for global MATLAB commands."""

from talon import Module, actions, app

mod = Module()


def _matlab_global_shortcut(base_shortcut: str) -> str:
    modifier = "cmd" if app.platform == "mac" else "ctrl"
    return f"{modifier}-{base_shortcut}"


@mod.action_class
class Actions:
    def matlab_global_panel(panel_name: str) -> None:
        """Focus MATLAB and open a global panel by name."""
        if panel_name == "command":
            actions.user.switcher_focus("matlab")
            actions.key(_matlab_global_shortcut("0"))
            return
        if panel_name == "editor":
            actions.user.switcher_focus("matlab")
            actions.key(_matlab_global_shortcut("shift-0"))
            return
        raise ValueError(f"Unknown MATLAB panel: {panel_name}")
