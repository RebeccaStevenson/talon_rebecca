"""Behaviours, captures & actions that aren't in a dedicated module yet."""

from talon import Module, Context, actions, imgui, app, clip
from typing import Optional, List
from pathlib import Path
import os
import shlex
import subprocess
import webbrowser
import logging

LOGGER = logging.getLogger()


module = Module()


# Stores the previous microphone, for when the microphone is disabled with
# `toggle_mic_off`
_previous_mic = None


@module.action_class
class ModuleActions:
    def open_file() -> None:
        """Bring up a dialogue to open a file."""

    def cancel() -> None:
        """Cancel the current "thing" - e.g. by press escape.

        (Note this is not meant to be the most powerful context exiting command
        available.)"""
        
        actions.key("escape")

    def opening_number_action(number: int) -> None:
        """Context-specific command that fires on an opening number."""
        # Override this with any DWIM number action that is useful in a specific
        # context.
        #
        # This is defined here so the DFA graph doesn't have to be recompiled
        # every time there is a context switch between states with/without
        # opening number actions. This is particularly important in Emacs,
        # specifically popping up autocomplete boxes - ideally, a recompile
        # shouldn't be necessary when the autocomplete box pops up, even if
        # items can be selected by number.
        print("Got repeat {number} without prior command, ignoring.")
        app.notify(
            "Number DWIM", "No opening number actions available in this context."
        )




    def debug(text: str):
        """Print and notify with a string."""
        LOGGER.info(text)
        app.notify("Talon Debug", text)




# TODO: Dedicated settings file?
global_context = Context()
global_context.settings["imgui.dark_mode"] = 1
global_context.settings["imgui.scale"] = 1.8


@global_context.action_class("self")
class GlobalActions:
    pass


@global_context.action_class("app")
class AppActions:
    def path() -> str:
        raise NotImplementedError("`path` action not implemented in this context.")


windows_context = Context(name="unsorted_windows")
windows_context.matches = r"os: windows"
linux_context = Context(name="unsorted_linux")
linux_context.matches = r"os: linux"
mac_context = Context(name="unsorted_mac")
mac_context.matches = r"os: mac"
win_linux_context = Context(name="unsorted_win_linux")
win_linux_context.matches = r"""
os: linux
os: windows
"""


@win_linux_context.action_class("self")
class WinLinuxActions:
    def open_file() -> None:
        actions.key("ctrl-o")


@mac_context.action_class("self")
class MacActions:
    def open_file() -> None:
        actions.key("cmd-o")
