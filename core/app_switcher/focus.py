"""Shared focus helpers for running Talon apps/windows."""

from __future__ import annotations

from typing import Optional

from talon import ui

from user.talon_rebecca.core.app_switcher.matching import hierarchical_name_match


def focus_running_app(app_name: Optional[str] = None, title: Optional[str] = None) -> None:
    """Focus a running app by app name, window title, or both."""
    assert app_name or title, "Must provide `app_name` and/or `title`."

    apps = ui.apps(background=False)
    if app_name:
        apps = hierarchical_name_match(
            app_name,
            [(app.name, app) for app in apps],
            True,
            True,
            True,
        )
        if not apps:
            raise IndexError(f'Running app not found matching name: "{app_name}"')

    if title:
        apps = hierarchical_name_match(
            title,
            [(app.active_window.title, app) for app in apps],
            True,
            True,
            True,
        )
        if not apps:
            raise IndexError(f'Running app not found matching title: "{title}"')

    try:
        apps[0].focus()
    except Exception as error:
        raise IndexError(f'Problem focussing app: "{error}"') from error
