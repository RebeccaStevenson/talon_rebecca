from __future__ import annotations

from pathlib import Path

from talon import Module, actions, app

mod = Module()

_SCRIPT_PATH = Path("/Users/rebec/localFiles/check_break_timer.py")


@mod.action_class
class Actions:
    def break_timer_show_remaining():
        """Display the remaining time until the next BreakTimer break."""
        script_path = _SCRIPT_PATH
        if not script_path.exists():
            message = f"BreakTimer script missing: {script_path}"
            app.notify(message)
            raise FileNotFoundError(message)

        actions.user.run_command_in_new_terminal(
            command=str(script_path),
            press_enter=True,
            close_after=False,
            post_command_delay="200ms",
        )
