"""Talon actions for focusing and launching common desktop programs."""

from typing import Any, Optional

from talon import Context, Module, actions, app, ui

from user.talon_rebecca.core.app_switcher.focus import focus_running_app
from user.talon_rebecca.core.app_switcher.matching import (
    heirarchical_name_match as _heirarchical_name_match,
    hierarchical_name_match as _hierarchical_name_match,
)
from user.talon_rebecca.system.program_specs import PROGRAM_SPECS
from user.talon_rebecca.system.windows_launch import launch_program_windows


module = Module()


def _open_program(spec_name: str) -> None:
    spec = PROGRAM_SPECS[spec_name]
    if spec.launch_only:
        actions.user.launch_fuzzy(spec.start_name)
        return

    actions.user.switch_or_start(
        start_name=spec.start_name,
        focus_name=spec.focus_name,
        focus_title=spec.focus_title,
        start_delay=spec.start_delay,
    )


def _launch_exact(program_name: str) -> None:
    """Launch a program by explicit path or bundle name."""
    ui.launch(path=program_name)


def _heirarchical_name_match_action(
    target_name: str,
    candidates: list[tuple[str, Any]],
    match_start: bool,
    match_anywhere: bool,
    match_fuzzy: bool,
) -> list[Any]:
    """Compatibility wrapper for the historical misspelled action name."""
    return _heirarchical_name_match(
        target_name,
        candidates,
        match_start,
        match_anywhere,
        match_fuzzy,
    )


def _hierarchical_name_match_action(
    target_name: str,
    candidates: list[tuple[str, Any]],
    match_start: bool,
    match_anywhere: bool,
    match_fuzzy: bool,
) -> list[Any]:
    """Match a name to candidates using exact, prefix, substring, then fuzzy search."""
    return _hierarchical_name_match(
        target_name,
        candidates,
        match_start,
        match_anywhere,
        match_fuzzy,
    )


def _focus_program(
    app_name: Optional[str] = None, title: Optional[str] = None
) -> None:
    """Focus a program by either the app name, title, or both."""
    focus_running_app(app_name=app_name, title=title)


def _switch_or_start(
    start_name: str,
    focus_name: Optional[str] = None,
    focus_title: Optional[str] = None,
    start_delay: str = "2000ms",
) -> None:
    """Switch to a program, starting it if necessary."""
    # Revert to the same name used to start the program when no focus
    # parameters have been set.
    if not (focus_name or focus_title):
        focus_name = start_name

    try:
        actions.user.focus(app_name=focus_name, title=focus_title)
    # Sometimes talon's ui.focus() will pop a `UIErr` because it can't find
    # a window for a running program - in these cases, we assume the program
    # needs to be relaunched.
    except (IndexError, ui.UIErr):
        actions.user.launch_fuzzy(start_name)
        # Give it time to start up
        actions.sleep(start_delay)
        try:
            actions.user.focus(app_name=focus_name, title=focus_title)
        except (IndexError, ui.UIErr):
            print(f"Could not focus newly started program: {focus_name}. Skipping.")
    # Give it time to focus
    actions.sleep("200ms")


@module.action_class
class Actions:
    """Class holding cleanly named switcher functions"""

    def launch_exact(program_name):
        """Launch a program exactly matching `name`."""
        # TODO: Exact name match, but not path match, on Windows?
        _launch_exact(program_name)

    def launch_fuzzy(program_name):
        """Launch a program matching `name` - will use fuzzy heuristics to find the program."""

    def heirarchical_name_match(
        target_name, candidates, match_start, match_anywhere, match_fuzzy
    ):
        """Compatibility wrapper for the historical misspelled action name."""
        return _heirarchical_name_match_action(
            target_name, candidates, match_start, match_anywhere, match_fuzzy
        )

    def hierarchical_name_match(
        target_name, candidates, match_start, match_anywhere, match_fuzzy
    ):
        """Match a name to candidates using exact, prefix, substring, then fuzzy search."""
        return _hierarchical_name_match_action(
            target_name, candidates, match_start, match_anywhere, match_fuzzy
        )

    def focus(app_name=None, title=None):
        """Focus a program by either the app name, title, or both."""
        _focus_program(app_name=app_name, title=title)

    def switch_or_start(
        start_name, focus_name=None, focus_title=None, start_delay="2000ms"
    ):
        """Switch to a program, starting it if necessary."""
        _switch_or_start(
            start_name=start_name,
            focus_name=focus_name,
            focus_title=focus_title,
            start_delay=start_delay,
        )

    # TODO: Go through each of these and check they all work?

    def open_firefox():
        """Switch to firefox, starting it if necessary."""
        _open_program("firefox")

    def open_chrome():
        """Switch to chrome, starting it if necessary."""
        _open_program("chrome")

    def open_discord():
        """Switch to discord, starting it if necessary."""
        # FIXME: Won't launch Discord on Windows - but does switch to it if it's
        #   running and not minimized to the tray.
        _open_program("discord")

    def open_slack():
        """Switch to slack, starting it if necessary."""
        # If slack is minimized to the tray, focussing it causes weird errors -
        # so just restart it. This functions the same as focussing it.
        _open_program("slack")

    def open_rider():
        """Switch to rider, starting it if necessary."""
        _open_program("rider")

    def open_blender():
        """Switch to blender, starting it if necessary."""
        _open_program("blender")

    def open_unreal_engine():
        """Switch to unreal_engine, starting it if necessary."""
        _open_program("unreal_engine")

    def open_task_manager():
        """Switch to task_manager, starting it if necessary."""
        _open_program("task_manager")

    # TODO: Remove this? Just leave the Windows Terminal command?
    def open_command_prompt():
        """Switch to command_prompt, starting it if necessary."""
        # Doubles as talon's output
        _open_program("command_prompt")

    # TODO: Remove this? Just leave the Windows Terminal command?
    def open_powershell():
        """Switch to powershell, starting it if necessary."""
        # Doubles as talon's output
        _open_program("powershell")

    def open_windows_terminal():
        """Switch to Windows Terminal, starting it if necessary."""
        _open_program("windows_terminal")

    def open_windows_explorer():
        """Open windows explorer (specifically, open the file browser)."""
        # FIXME: Doesn't start file explorer
        _open_program("windows_explorer")

    def open_epic_games():
        """Switch to epic_games, starting it if necessary."""
        _open_program("epic_games")

    def open_emacs():
        """Switch to emacs, starting it if necessary."""
        # TODO: An action that focuses based on exe AND title
        try:
            actions.user.focus(app_name="vcxsrv", title="emacs")
            return
        except IndexError:
            pass
        try:
            actions.user.focus(app_name="emacs")
            return
        except IndexError:
            pass
        try:
            # Prefer my custom WSL Emacs shortcut on Windows
            actions.user.launch_fuzzy("WSL Emacs")
            return
        except ValueError:
            pass
        # But if all else fails, just use a basic match.
        actions.user.launch_fuzzy("emacs")

    def open_whatsapp():
        """Switch to whatsapp, starting it if necessary."""
        _open_program("whatsapp")

    def focus_talon_log():
        """Switch to the talon log."""
        actions.user.focus(app_name="talon", title="Talon Log")

    def focus_talon_repl():
        """Switch to the talon repl."""
        # These titles rely on fuzzy match
        if app.platform == "windows":
            actions.user.focus(app_name="Console", title="Talon REPL")
        else:
            actions.user.focus(title="Talon REPL")


windows_context = Context(name="programs_windows")
windows_context.matches = r"os: windows"


@windows_context.action_class("self")
class WindowsActions:
    def launch_exact(program_name: str) -> None:
        launch_program_windows(
            program_name,
            match_start=False,
            match_fuzzy=False,
        )

    def launch_fuzzy(program_name: str) -> None:
        launch_program_windows(
            program_name,
            match_start=True,
            match_fuzzy=True,
        )
