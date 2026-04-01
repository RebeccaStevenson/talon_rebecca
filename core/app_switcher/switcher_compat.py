"""Compatibility actions for switcher behavior removed from refreshed community."""

import re

from talon import Module, actions, ui

mod = Module()


@mod.action_class
class Actions:
    def switcher_focus_app_title(app_name: str, regex: str) -> None:
        """Focus a visible window whose app name contains app_name and title matches regex."""
        pattern = re.compile(regex) if regex else None

        for window in ui.windows():
            title = getattr(window, "title", "") or ""
            window_app = getattr(window, "app", None)
            window_app_name = getattr(window_app, "name", "")

            if getattr(window, "hidden", False) or not title:
                continue
            if app_name != "*" and app_name not in window_app_name:
                continue
            if pattern is not None and not pattern.search(title):
                continue

            actions.user.switcher_focus_window(window)
            return
